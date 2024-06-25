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


// IP VLNV: xilinx.com:module_ref:steganography:1.0
// IP Revision: 1

(* X_CORE_INFO = "steganography,Vivado 2023.1" *)
(* CHECK_LICENSE_TYPE = "design_1_steganography_0_1,steganography,{}" *)
(* CORE_GENERATION_INFO = "design_1_steganography_0_1,steganography,{x_ipProduct=Vivado 2023.1,x_ipVendor=xilinx.com,x_ipLibrary=module_ref,x_ipName=steganography,x_ipVersion=1.0,x_ipCoreRevision=1,x_ipLanguage=VERILOG,x_ipSimLanguage=MIXED,DATA_WIDTH=32,ADDR_WIDTH=16,NUM_BYTES=4,REG_WIDTH=32,FF_WIDTH=8}" *)
(* IP_DEFINITION_SOURCE = "module_ref" *)
(* DowngradeIPIdentifiedWarnings = "yes" *)
module design_1_steganography_0_1 (
  sys_clk,
  ps_enb,
  debug_data1,
  debug_data2,
  control_signal,
  picture_size,
  message_size,
  respond_signal,
  image_ena,
  image_rddataa,
  image_wea,
  image_addra,
  image_clka,
  image_rsta,
  secret_ena,
  secret_rddataa,
  secret_wea,
  secret_addra,
  secret_clka,
  secret_rsta,
  image_enb,
  image_wrdatab,
  image_web,
  image_addrb,
  image_clkb,
  image_rstb,
  secret_enb,
  secret_wrdatab,
  secret_web,
  secret_addrb,
  secret_clkb,
  secret_rstb
);

(* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME sys_clk, FREQ_HZ 100000000, FREQ_TOLERANCE_HZ 0, PHASE 0.0, CLK_DOMAIN design_1_zynq_ultra_ps_e_0_0_pl_clk0, INSERT_VIP 0" *)
(* X_INTERFACE_INFO = "xilinx.com:signal:clock:1.0 sys_clk CLK" *)
input wire sys_clk;
output wire ps_enb;
output wire [31 : 0] debug_data1;
output wire [31 : 0] debug_data2;
input wire [31 : 0] control_signal;
input wire [31 : 0] picture_size;
input wire [31 : 0] message_size;
output wire [31 : 0] respond_signal;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEA EN" *)
output wire image_ena;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEA DOUT" *)
input wire [31 : 0] image_rddataa;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEA WE" *)
output wire [3 : 0] image_wea;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEA ADDR" *)
output wire [15 : 0] image_addra;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEA CLK" *)
output wire image_clka;
(* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME BRAM_IMAGEA, MASTER_TYPE BRAM_CTRL, MEM_ECC NONE, MEM_WIDTH 32, MEM_SIZE 262144, READ_WRITE_MODE READ_WRITE, READ_LATENCY 1" *)
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEA RST" *)
output wire image_rsta;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETA EN" *)
output wire secret_ena;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETA DOUT" *)
input wire [31 : 0] secret_rddataa;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETA WE" *)
output wire [3 : 0] secret_wea;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETA ADDR" *)
output wire [15 : 0] secret_addra;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETA CLK" *)
output wire secret_clka;
(* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME BRAM_SECRETA, MASTER_TYPE BRAM_CTRL, MEM_ECC NONE, MEM_WIDTH 32, MEM_SIZE 262144, READ_WRITE_MODE READ_WRITE, READ_LATENCY 1" *)
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETA RST" *)
output wire secret_rsta;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEB EN" *)
output wire image_enb;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEB DIN" *)
output wire [31 : 0] image_wrdatab;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEB WE" *)
output wire [3 : 0] image_web;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEB ADDR" *)
output wire [15 : 0] image_addrb;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEB CLK" *)
output wire image_clkb;
(* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME BRAM_IMAGEB, MASTER_TYPE BRAM_CTRL, MEM_ECC NONE, MEM_WIDTH 32, MEM_SIZE 262144, READ_WRITE_MODE READ_WRITE, READ_LATENCY 1" *)
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_IMAGEB RST" *)
output wire image_rstb;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETB EN" *)
output wire secret_enb;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETB DIN" *)
output wire [31 : 0] secret_wrdatab;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETB WE" *)
output wire [3 : 0] secret_web;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETB ADDR" *)
output wire [15 : 0] secret_addrb;
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETB CLK" *)
output wire secret_clkb;
(* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME BRAM_SECRETB, MASTER_TYPE BRAM_CTRL, MEM_ECC NONE, MEM_WIDTH 32, MEM_SIZE 262144, READ_WRITE_MODE READ_WRITE, READ_LATENCY 1" *)
(* X_INTERFACE_INFO = "xilinx.com:interface:bram:1.0 BRAM_SECRETB RST" *)
output wire secret_rstb;

  steganography #(
    .DATA_WIDTH(32),
    .ADDR_WIDTH(16),
    .NUM_BYTES(4),
    .REG_WIDTH(32),
    .FF_WIDTH(8)
  ) inst (
    .sys_clk(sys_clk),
    .ps_enb(ps_enb),
    .debug_data1(debug_data1),
    .debug_data2(debug_data2),
    .control_signal(control_signal),
    .picture_size(picture_size),
    .message_size(message_size),
    .respond_signal(respond_signal),
    .image_ena(image_ena),
    .image_rddataa(image_rddataa),
    .image_wea(image_wea),
    .image_addra(image_addra),
    .image_clka(image_clka),
    .image_rsta(image_rsta),
    .secret_ena(secret_ena),
    .secret_rddataa(secret_rddataa),
    .secret_wea(secret_wea),
    .secret_addra(secret_addra),
    .secret_clka(secret_clka),
    .secret_rsta(secret_rsta),
    .image_enb(image_enb),
    .image_wrdatab(image_wrdatab),
    .image_web(image_web),
    .image_addrb(image_addrb),
    .image_clkb(image_clkb),
    .image_rstb(image_rstb),
    .secret_enb(secret_enb),
    .secret_wrdatab(secret_wrdatab),
    .secret_web(secret_web),
    .secret_addrb(secret_addrb),
    .secret_clkb(secret_clkb),
    .secret_rstb(secret_rstb)
  );
endmodule
