# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

def rotar_MSB_LSB_4(inversor):
    lista_MSB_LSB_4=[0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]
    return lista_MSB_LSB_4[inversor]

def display_7seg_mal(valor):
    seg7_mal=[119,65,59,107,77,110,126,67,127,111]
    return seg7_mal[valor]

def display_7seg_cath(valor):
    seg7_cath=[63,6,91,79,102,109,125,7,127,111]
    return seg7_cath[valor]
    
async def reset():
    dut.ui_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    return

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.uio_in.value = 0
    
    reset()

    dut._log.info("Test project 0 behaviour")
    for i in range(10):
        dut.ui_in.value = rotar_MSB_LSB_4(i)
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == display_7seg_mal(i)

    reset()
    
    dut._log.info("Test project 1 behaviour")
    for i in range(10):
        dut.ui_in.value = 1
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        assert dut.uo_out.value == display_7seg_cath(i)
        await ClockCycles(dut.clk, 1)

    

    
    # Set the input values you want to test
    #dut.ui_in.value = 3

    # Wait for one clock cycle to see the output values
    #await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    #assert dut.uo_out.value == 107

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
