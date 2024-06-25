// (c) Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// (c) Copyright 2022-2024 Advanced Micro Devices, Inc. All rights reserved.
// 
// This file contains confidential and proprietary information
// of AMD and is protected under U.S. and international copyright
// and other intellectual property laws.
// 
// DISCLAIMER
// This disclaimer is not a license and does not grant any
// rights to the materials distributed herewith. Except as
// otherwise provided in a valid license issued to you by
// AMD, and to the maximum extent permitted by applicable
// law: (1) THESE MATERIALS ARE MADE AVAILABLE "AS IS" AND
// WITH ALL FAULTS, AND XILINX HEREBY DISCLAIMS ALL WARRANTIES
// AND CONDITIONS, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING
// BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, NON-
// INFRINGEMENT, OR FITNESS FOR ANY PARTICULAR PURPOSE; and
// (2) AMD shall not be liable (whether in contract or tort,
// including negligence, or under any other theory of
// liability) for any loss or damage of any kind or nature
// related to, arising under or in connection with these
// materials, including for any direct, or any indirect,
// special, incidental, or consequential loss or damage
// (including loss of data, profits, goodwill, or any type of
// loss or damage suffered as a result of any action brought
// by a third party) even if such damage or loss was
// reasonably foreseeable or AMD had been advised of the
// possibility of the same.
// 
// CRITICAL APPLICATIONS
// AMD products are not designed or intended to be fail-
// safe, or for use in any application requiring fail-safe
// performance, such as life-support or safety devices or
// systems, Class III medical devices, nuclear facilities,
// applications related to the deployment of airbags, or any
// other applications that could lead to death, personal
// injury, or severe property or environmental damage
// (individually and collectively, "Critical
// Applications"). Customer assumes the sole risk and
// liability of any use of AMD products in Critical
// Applications, subject only to applicable laws and
// regulations governing limitations on product liability.
// 
// THIS COPYRIGHT NOTICE AND DISCLAIMER MUST BE RETAINED AS
// PART OF THIS FILE AT ALL TIMES.
// 
// DO NOT MODIFY THIS FILE.


// IP VLNV: xilinx.com:module_ref:bram_ctrl:1.0
// IP Revision: 1

`timescale 1ns/1ps

(* IP_DEFINITION_SOURCE = "module_ref" *)
(* DowngradeIPIdentifiedWarnings = "yes" *)
module design_1_bram_ctrl_0_0 (
  ps_enb,
  en,
  rddata,
  wrdata,
  we,
  addr,
  clk,
  rst,
  ps_en,
  ps_dout,
  ps_din,
  ps_we,
  ps_addr,
  ps_clk,
  ps_rst,
  pl_en,
  pl_dout,
  pl_din,
  pl_we,
  pl_addr,
  pl_clk,
  pl_rst
);

input wire ps_enb;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_PORTA EN" *)
output wire en;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_PORTA DOUT" *)
input wire [31 : 0] rddata;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_PORTA DIN" *)
output wire [31 : 0] wrdata;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_PORTA WE" *)
output wire [3 : 0] we;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_PORTA ADDR" *)
output wire [31 : 0] addr;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_PORTA CLK" *)
output wire clk;
(* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME BRAM_PORTA, MASTER_TYPE BRAM_CTRL, MEM_ECC NONE, MEM_WIDTH 32, MEM_SIZE 262144, READ_WRITE_MODE READ_WRITE, READ_LATENCY 1" *)
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_PORTA RST" *)
output wire rst;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLA EN" *)
input wire ps_en;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLA DOUT" *)
output wire [31 : 0] ps_dout;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLA DIN" *)
input wire [31 : 0] ps_din;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLA WE" *)
input wire [3 : 0] ps_we;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLA ADDR" *)
input wire [31 : 0] ps_addr;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLA CLK" *)
input wire ps_clk;
(* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME BRAM_CTRLA, MASTER_TYPE BRAM_CTRL, MEM_ECC NONE, MEM_WIDTH 32, MEM_SIZE 262144, READ_WRITE_MODE READ_WRITE, READ_LATENCY 1" *)
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLA RST" *)
input wire ps_rst;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLB EN" *)
input wire pl_en;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLB DOUT" *)
output wire [31 : 0] pl_dout;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLB DIN" *)
input wire [31 : 0] pl_din;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLB WE" *)
input wire [3 : 0] pl_we;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLB ADDR" *)
input wire [31 : 0] pl_addr;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLB CLK" *)
input wire pl_clk;
(* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME BRAM_CTRLB, MASTER_TYPE BRAM_CTRL, MEM_ECC NONE, MEM_WIDTH 32, MEM_SIZE 262144, READ_WRITE_MODE READ_WRITE, READ_LATENCY 1" *)
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_CTRLB RST" *)
input wire pl_rst;

  bram_ctrl #(
    .ADDR_WIDTH(32),
    .DATA_WIDTH(32),
    .NUM_BYTES(4)
  ) inst (
    .ps_enb(ps_enb),
    .en(en),
    .rddata(rddata),
    .wrdata(wrdata),
    .we(we),
    .addr(addr),
    .clk(clk),
    .rst(rst),
    .ps_en(ps_en),
    .ps_dout(ps_dout),
    .ps_din(ps_din),
    .ps_we(ps_we),
    .ps_addr(ps_addr),
    .ps_clk(ps_clk),
    .ps_rst(ps_rst),
    .pl_en(pl_en),
    .pl_dout(pl_dout),
    .pl_din(pl_din),
    .pl_we(pl_we),
    .pl_addr(pl_addr),
    .pl_clk(pl_clk),
    .pl_rst(pl_rst)
  );
endmodule
