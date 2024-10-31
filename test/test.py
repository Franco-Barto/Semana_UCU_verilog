# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

def rotar_MSB_LSB_4(inversor):
    lista_MSB_LSB_4=[0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]
    return lista_MSB_LSB_4[inversor]
    
def rotar_MSB_LSB_3(inversor):
    lista_MSB_LSB_3=[0,4,2,6,1,5,3,7]
    return lista_MSB_LSB_3[inversor]

def display_7seg_mal(valor):
    seg7_mal=[119,65,59,107,77,110,126,67,127,111]
    return seg7_mal[valor]
    
def display_7seg_cath(valor):
    seg7_cath_9cd=[63,6,91,79,102,109,125,7,127,111]
    return seg7_cath_9cd[valor]

def display_7seg_cath_9sd(valor):
    seg7_cath_9sd=[63,6,91,79,102,109,125,7,127,103]
    return seg7_cath_9sd[valor]    
    
def display_7seg_cath_6sa(valor):
    seg7_cath_9cd_6sa=[63,6,91,79,102,109,124,7,127,111]
    return seg7_cath_9cd_6sa[valor]

def display_7seg_an(valor):
    return 127-display_7seg_cath(valor)

async def reset(dut): 
    dut.ui_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    
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
   
    await reset(dut)

    dut._log.info("Test project 0 behaviour")
    for i in range(10):
        dut.ui_in.value = rotar_MSB_LSB_4(i)
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == display_7seg_mal(i)

    await reset(dut)
    
    dut._log.info("Test project 1 behaviour")
    for i in range(11):        
        dut.ui_in.value = 16
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == display_7seg_cath_9sd(i%10)
        dut.ui_in.value = 17
        await ClockCycles(dut.clk, 1)

    await reset(dut)

    dut._log.info("Test project 2 behaviour")
    for i in range(8):
        dut.ui_in.value = rotar_MSB_LSB_3(i)+32
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == display_7seg_cath(i)
    
    await reset(dut)

    dut._log.info("Test project 3 behaviour")
    for i in range(8):
        dut.ui_in.value = rotar_MSB_LSB_3(i)+48
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == display_7seg_cath(i)

    await reset(dut)
    
    dut._log.info("Test project 4 behaviour")
    for i in range(8):
        dut.ui_in.value = rotar_MSB_LSB_3(i)+64
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == display_7seg_cath_6sa(i)

    await reset(dut)
    
    dut._log.info("Test project 5 behaviour")
    for i in range(9):        
        dut.ui_in.value = 80
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == display_7seg_cath_6sa(i%8)
        dut.ui_in.value = 81
        await ClockCycles(dut.clk, 1)
        
    await reset(dut)
    
    dut._log.info("Test project 6 behaviour")
    for i in range(10):        
        dut.ui_in.value = 96
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == display_7seg_cath(i%10)
        dut.ui_in.value = 97
        await ClockCycles(dut.clk, 1)

    await reset(dut)
    
    dut._log.info("Test project 7 behaviour")
    for i in range(9):        
        dut._log.info("Check at "+str(i))
        dut.ui_in.value = 112
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == display_7seg_an(i%8)
        dut.ui_in.value = 113
        await ClockCycles(dut.clk, 1)
        

    

    
