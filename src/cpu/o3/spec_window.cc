/*
 * Copyright (c) 2012 ARM Limited
 * All rights reserved
 *
 * The license below extends only to copyright in the software and shall
 * not be construed as granting a license to any other intellectual
 * property including but not limited to intellectual property relating
 * to a hardware implementation of the functionality of the software
 * licensed hereunder.  You may use the software subject to the license
 * terms below provided that you ensure that this notice is replicated
 * unmodified and in its entirety in all distributions of the software,
 * modified or unmodified, in source code or in binary form.
 *
 * Copyright (c) 2004-2006 The Regents of The University of Michigan
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include "cpu/o3/spec_window.hh"

#include <list>

#include "base/logging.hh"
#include "cpu/o3/dyn_inst.hh"
#include "cpu/o3/limits.hh"
#include "debug/Fetch.hh"
#include "debug/ROB.hh"
#include "debug/SPECWINDOW.hh"
#include "params/BaseO3CPU.hh"

namespace gem5
{

namespace o3
{

SPECWINDOW::SPECWINDOW(CPU *_cpu, const BaseO3CPUParams &params)
    : robPolicy(params.smtROBPolicy),
      cpu(_cpu),
      numEntries(params.numROBEntries),
      squashWidth(params.squashWidth),
      numInstsInSpecWindow(0),
      numThreads(params.numThreads),
      stats(_cpu)
{
    //Figure out rob policy
    if (robPolicy == SMTQueuePolicy::Dynamic) {
        //Set Max Entries to Total ROB Capacity
        for (ThreadID tid = 0; tid < numThreads; tid++) {
            maxEntries[tid] = numEntries;
        }

    } else if (robPolicy == SMTQueuePolicy::Partitioned) {
        DPRINTF(Fetch, "ROB sharing policy set to Partitioned\n");

        //@todo:make work if part_amt doesnt divide evenly.
        int part_amt = numEntries / numThreads;

        //Divide ROB up evenly
        for (ThreadID tid = 0; tid < numThreads; tid++) {
            maxEntries[tid] = part_amt;
        }

    } else if (robPolicy == SMTQueuePolicy::Threshold) {
        DPRINTF(Fetch, "ROB sharing policy set to Threshold\n");

        int threshold =  params.smtROBThreshold;;

        //Divide up by threshold amount
        for (ThreadID tid = 0; tid < numThreads; tid++) {
            maxEntries[tid] = threshold;
        }
    }

    for (ThreadID tid = numThreads; tid < MaxThreads; tid++) {
        maxEntries[tid] = 0;
    }

    resetState();
}

void
SPECWINDOW::resetState()
{
    for (ThreadID tid = 0; tid  < MaxThreads; tid++) {
        threadEntries[tid] = 0;
        squashIt[tid] = instList[tid].end();
        squashedSeqNum[tid] = 0;
        doneSquashing[tid] = true;
    }
    numInstsInSpecWindow = 0;

    // Initialize the "universal" ROB head & tail point to invalid
    // pointers
    head = instList[0].end();
    tail = instList[0].end();
}

std::string
SPECWINDOW::name() const
{
    return cpu->name() + ".spec_window";
}

void
SPECWINDOW::setActiveThreads(std::list<ThreadID> *at_ptr)
{
    DPRINTF(SPECWINDOW, "Setting active threads list pointer.\n");
    activeThreads = at_ptr;
}

void
SPECWINDOW::drainSanityCheck() const
{
    for (ThreadID tid = 0; tid  < numThreads; tid++)
        assert(instList[tid].empty());
    assert(isEmpty());
}

void
SPECWINDOW::takeOverFrom()
{
    resetState();
}

void
SPECWINDOW::resetEntries()
{
    if (robPolicy != SMTQueuePolicy::Dynamic || numThreads > 1) {
        auto active_threads = activeThreads->size();

        for (ThreadID tid : *activeThreads) {
            if (robPolicy == SMTQueuePolicy::Partitioned) {
                maxEntries[tid] = numEntries / active_threads;
            } else if (robPolicy == SMTQueuePolicy::Threshold &&
                       active_threads == 1) {
                maxEntries[tid] = numEntries;
            }
        }
    }
}

int
SPECWINDOW::entryAmount(ThreadID num_threads)
{
    if (robPolicy == SMTQueuePolicy::Partitioned) {
        return numEntries / num_threads;
    } else {
        return 0;
    }
}

int
SPECWINDOW::countInsts()
{
    int total = 0;

    for (ThreadID tid = 0; tid < numThreads; tid++)
        total += countInsts(tid);

    return total;
}

size_t
SPECWINDOW::countInsts(ThreadID tid)
{
    return instList[tid].size();
}

void
SPECWINDOW::insertInst(const DynInstPtr &inst)
{
    assert(inst);

    stats.writes++;

    DPRINTF(SPECWINDOW, "Adding inst PC %s to the ROB.\n", inst->pcState());

    assert(numInstsInSpecWindow != numEntries);

    ThreadID tid = inst->threadNumber;

    instList[tid].push_back(inst);

    //Set Up head iterator if this is the 1st instruction in the ROB
    if (numInstsInSpecWindow == 0) {
        head = instList[tid].begin();
        assert((*head) == inst);
    }

    //Must Decrement for iterator to actually be valid  since __.end()
    //actually points to 1 after the last inst
    tail = instList[tid].end();
    tail--;

    inst->setInROB();

    ++numInstsInSpecWindow;
    ++threadEntries[tid];

    assert((*tail) == inst);

    DPRINTF(SPECWINDOW, "[tid:%i] Now has %d instructions.\n", tid,
            threadEntries[tid]);
}

void
SPECWINDOW::retireHead(ThreadID tid)
{
    stats.writes++;

    assert(numInstsInSpecWindow > 0);

    // Get the head ROB instruction by copying it and remove it from the list
    InstIt head_it = instList[tid].begin();

    DynInstPtr head_inst = std::move(*head_it);
    instList[tid].erase(head_it);

    assert(head_inst->readyToCommit());

    DPRINTF(SPECWINDOW, "[tid:%i] Retiring head instruction, "
            "instruction PC %s, [sn:%llu]\n", tid, head_inst->pcState(),
            head_inst->seqNum);

    --numInstsInSpecWindow;
    --threadEntries[tid];

    head_inst->clearInROB();
    head_inst->setCommitted();

    //Update "Global" Head of ROB
    updateHeadSpecWindow();

    // @todo: A special case is needed if the instruction being
    // retired is the only instruction in the ROB; otherwise the tail
    // iterator will become invalidated.
    cpu->removeFrontInst(head_inst);
}

void
SPECWINDOW::retireHeadSpecWindow(ThreadID tid)
{
    stats.writes++;

    assert(numInstsInSpecWindow > 0);

    // Get the head ROB instruction by copying it and remove it from the list
    InstIt head_it = instList[tid].begin();

    DynInstPtr head_inst = std::move(*head_it);
    instList[tid].erase(head_it);
    assert(head_inst->readyToCommit());

    DPRINTF(SPECWINDOW, "[tid:%i] Retiring head instruction, "
            "instruction PC %s, [sn:%llu]\n", tid, head_inst->pcState(),
            head_inst->seqNum);

    --numInstsInSpecWindow;
    --threadEntries[tid];

    //Update "Global" Head of ROB
    updateHeadSpecWindow();
}

bool
SPECWINDOW::isHeadReady(ThreadID tid)
{
    stats.reads++;
    if (threadEntries[tid] != 0) {
        return instList[tid].front()->readyToCommit();
    }

    return false;
}

bool
SPECWINDOW::canCommit()
{
    //@todo: set ActiveThreads through ROB or CPU
    for (ThreadID tid : *activeThreads) {
        if (isHeadReady(tid)) {
            return true;
        }
    }

    return false;
}

unsigned
SPECWINDOW::numFreeEntries()
{
    return numEntries - numInstsInSpecWindow;
}

unsigned
SPECWINDOW::numFreeEntries(ThreadID tid)
{
    return maxEntries[tid] - threadEntries[tid];
}

void
SPECWINDOW::doSquash(ThreadID tid)
{
    stats.writes++;
    DPRINTF(SPECWINDOW, "[tid:%i] Squashing instructions until [sn:%llu].\n",
            tid, squashedSeqNum[tid]);

    //dfence_opt
    //assert(squashIt[tid] != instList[tid].end());
    if (squashIt[tid] == instList[tid].end()){
        return;
    }

    if ((*squashIt[tid])->seqNum < squashedSeqNum[tid]) {
        DPRINTF(SPECWINDOW, "[tid:%i] Done squashing instructions.\n",
                tid);

        squashIt[tid] = instList[tid].end();

        doneSquashing[tid] = true;
        return;
    }

    bool robTailUpdate = false;

    unsigned int numInstsToSquash = squashWidth;

    // If the CPU is exiting, squash all of the instructions
    // it is told to, even if that exceeds the squashWidth.
    // Set the number to the number of entries (the max).
    if (cpu->isThreadExiting(tid))
    {
        numInstsToSquash = numEntries;
    }

    for (int numSquashed = 0;
         numSquashed < numInstsToSquash &&
         squashIt[tid] != instList[tid].end() &&
         (*squashIt[tid])->seqNum > squashedSeqNum[tid];
         ++numSquashed)
    {
        DPRINTF(SPECWINDOW, "[tid:%i] Squashing instruction PC %s,\n",
                (*squashIt[tid])->threadNumber,
                (*squashIt[tid])->pcState());

        // Mark the instruction as squashed, and ready to commit so that
        // it can drain out of the pipeline.
        (*squashIt[tid])->setSquashed();

        (*squashIt[tid])->setCanCommit();


        if (squashIt[tid] == instList[tid].begin()) {
            DPRINTF(SPECWINDOW, "Reached head of instruction list while "
                    "squashing.\n");

            squashIt[tid] = instList[tid].end();

            doneSquashing[tid] = true;

            return;
        }

        InstIt tail_thread = instList[tid].end();
        tail_thread--;

        if ((*squashIt[tid]) == (*tail_thread))
            robTailUpdate = true;

        squashIt[tid]--;
    }


    // Check if ROB is done squashing.
    if ((*squashIt[tid])->seqNum <= squashedSeqNum[tid]) {
        DPRINTF(SPECWINDOW, "[tid:%i] Done squashing instructions.\n",
                tid);

        squashIt[tid] = instList[tid].end();

        doneSquashing[tid] = true;
    }

    if (robTailUpdate) {
        updateTail();
    }
}


void
SPECWINDOW::doSquashSpecWindow(ThreadID tid)
{
    stats.writes++;
    DPRINTF(SPECWINDOW, "[tid:%i] Squashing instructions until [sn:%llu].\n",
            tid, squashedSeqNum[tid]);

    //assert(squashIt[tid] != instList[tid].end());

    if (readHeadInst(tid)!= NULL &&
        squashedSeqNum[tid] > readHeadInst(tid)->seqNum){

        if ((*squashIt[tid])->seqNum < squashedSeqNum[tid]) {
            DPRINTF(SPECWINDOW, "[tid:%i] Done squashing instructions.\n",
                tid);

                squashIt[tid] = instList[tid].end();

                doneSquashing[tid] = true;
                return;
            }

            bool robTailUpdate = false;

            unsigned int numInstsToSquash = squashWidth;

            // If the CPU is exiting, squash all of the instructions
            // it is told to, even if that exceeds the squashWidth.
            // Set the number to the number of entries (the max).
            if (cpu->isThreadExiting(tid))
            {
                numInstsToSquash = numEntries;
            }

            for (int numSquashed = 0;
                numSquashed < numInstsToSquash &&
                squashIt[tid] != instList[tid].end() &&
                (*squashIt[tid])->seqNum > squashedSeqNum[tid];
                ++numSquashed)
                {
                DPRINTF(SPECWINDOW, "[tid:%i] Squashing instruction PC %s\n",
                    (*squashIt[tid])->threadNumber,
                    (*squashIt[tid])->pcState());

                if (squashIt[tid] == instList[tid].begin()) {
                    DPRINTF(SPECWINDOW, "Reached head of inst list while"
                        "squashing.\n");

                        squashIt[tid] = instList[tid].end();

                        doneSquashing[tid] = true;

                        return;
                    }

                    InstIt tail_thread = instList[tid].end();
                    tail_thread--;

                    if ((*squashIt[tid]) == (*tail_thread))
                    robTailUpdate = true;


                    squashIt[tid]--;

                DPRINTF(SPECWINDOW, "[tid:%i] Now has %d instructions.\n",
                    tid,
                    threadEntries[tid]);
                }


                // Check if ROB is done squashing.
                if ((*squashIt[tid])->seqNum <= squashedSeqNum[tid]) {
                    DPRINTF(SPECWINDOW, "[tid:%i] Done squashing insts.\n",
                        tid);

                        squashIt[tid] = instList[tid].end();

                        doneSquashing[tid] = true;
                    }

                    if (robTailUpdate) {
                        updateTail();
                    }
    }
}

void
SPECWINDOW::updateHeadSpecWindow()
{
    InstSeqNum lowest_num = 0;
    bool first_valid = true;

    // @todo: set ActiveThreads through ROB or CPU
    for (ThreadID tid : *activeThreads) {
        if (instList[tid].empty())
            continue;

        if (first_valid) {
            head = instList[tid].begin();
            lowest_num = (*head)->seqNum;
            first_valid = false;
            continue;
        }

        InstIt head_thread = instList[tid].begin();
        DynInstPtr head_inst = (*head_thread);
        assert(head_inst != 0);

        if (head_inst->seqNum < lowest_num) {
            head = head_thread;
            lowest_num = head_inst->seqNum;
        }
    }

    if (first_valid) {
        head = instList[0].end();
    }
}

void
SPECWINDOW::updateTail()
{
    tail = instList[0].end();
    bool first_valid = true;

    for (ThreadID tid : *activeThreads) {
        if (instList[tid].empty()) {
            continue;
        }

        // If this is the first valid then assign w/out
        // comparison
        if (first_valid) {
            tail = instList[tid].end();
            tail--;
            first_valid = false;
            continue;
        }

        // Assign new tail if this thread's tail is younger
        // than our current "tail high"
        InstIt tail_thread = instList[tid].end();
        tail_thread--;

        if ((*tail_thread)->seqNum > (*tail)->seqNum) {
            tail = tail_thread;
        }
    }
}


void
SPECWINDOW::squash(InstSeqNum squash_num, ThreadID tid)
{
    if (isEmpty(tid)) {
        DPRINTF(SPECWINDOW, "Does not need to squash due to being empty "
                "[sn:%llu]\n",
                squash_num);

        return;
    }

    DPRINTF(SPECWINDOW, "Starting to squash within the ROB.\n");

    specWindowStatus[tid] = ROBSquashing;

    doneSquashing[tid] = false;

    squashedSeqNum[tid] = squash_num;

    if (!instList[tid].empty()) {
        InstIt tail_thread = instList[tid].end();
        tail_thread--;

        squashIt[tid] = tail_thread;

        doSquashSpecWindow(tid);
    }
}

const DynInstPtr&
SPECWINDOW::readHeadInst(ThreadID tid)
{
    if (threadEntries[tid] != 0) {
        InstIt head_thread = instList[tid].begin();

        //assert((*head_thread)->isInROB());

        return *head_thread;
    } else {
        return dummyInst;
    }
}

DynInstPtr
SPECWINDOW::readTailInst(ThreadID tid)
{
    InstIt tail_thread = instList[tid].end();
    tail_thread--;

    return *tail_thread;
}

SPECWINDOW::SPECWINDOWStats::SPECWINDOWStats(statistics::Group *parent)
  : statistics::Group(parent, "spec_window"),
    ADD_STAT(reads, statistics::units::Count::get(),
        "The number of SPECWINDOW reads"),
    ADD_STAT(writes, statistics::units::Count::get(),
        "The number of SPECWINDOW writes")
{
}

DynInstPtr
SPECWINDOW::findInst(ThreadID tid, InstSeqNum squash_inst)
{
    for (InstIt it = instList[tid].begin(); it != instList[tid].end(); it++) {
        if ((*it)->seqNum == squash_inst) {
            return *it;
        }
    }
    return NULL;
}

} // namespace o3
} // namespace gem5
