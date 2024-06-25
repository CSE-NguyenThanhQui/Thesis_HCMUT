// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2023.1 (win64) Build 3865809 Sun May  7 15:05:29 MDT 2023
// Date        : Sat Jan 20 15:17:26 2024
// Host        : LAPTOP-NS7LM8D6 running 64-bit major release  (build 9200)
// Command     : write_verilog -force -mode synth_stub -rename_top decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix -prefix
//               decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix_ design_1_steganography_0_0_stub.v
// Design      : design_1_steganography_0_0
// Purpose     : Stub declaration of top-level module interface
// Device      : xczu3eg-sbva484-1-i
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
(* X_CORE_INFO = "steganography,Vivado 2023.1" *)
module decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix(sys_clk, ps_enb, debug_data1, debug_data2, 
  control_signal, picture_size, message_size, respond_signal, image_ena, image_rddataa, 
  image_wea, image_addra, image_clka, image_rsta, secret_ena, secret_rddataa, secret_wea, 
  secret_addra, secret_clka, secret_rsta, image_enb, image_wrdatab, image_web, image_addrb, 
  image_clkb, image_rstb, secret_enb, secret_wrdatab, secret_web, secret_addrb, secret_clkb, 
  secret_rstb)
/* synthesis syn_black_box black_box_pad_pin="ps_enb,debug_data1[15:0],debug_data2[15:0],control_signal[15:0],picture_size[15:0],message_size[15:0],respond_signal[15:0],image_ena,image_rddataa[15:0],image_wea[3:0],image_addra[15:0],image_rsta,secret_ena,secret_rddataa[15:0],secret_wea[3:0],secret_addra[15:0],secret_rsta,image_enb,image_wrdatab[15:0],image_web[3:0],image_addrb[15:0],image_rstb,secret_enb,secret_wrdatab[15:0],secret_web[3:0],secret_addrb[15:0],secret_rstb" */
/* synthesis syn_force_seq_prim="sys_clk" */
/* synthesis syn_force_seq_prim="image_clka" */
/* synthesis syn_force_seq_prim="secret_clka" */
/* synthesis syn_force_seq_prim="image_clkb" */
/* synthesis syn_force_seq_prim="secret_clkb" */;
  input sys_clk /* synthesis syn_isclock = 1 */;
  output ps_enb;
  output [15:0]debug_data1;
  output [15:0]debug_data2;
  input [15:0]control_signal;
  input [15:0]picture_size;
  input [15:0]message_size;
  output [15:0]respond_signal;
  output image_ena;
  input [15:0]image_rddataa;
  output [3:0]image_wea;
  output [15:0]image_addra;
  output image_clka /* synthesis syn_isclock = 1 */;
  output image_rsta;
  output secret_ena;
  input [15:0]secret_rddataa;
  output [3:0]secret_wea;
  output [15:0]secret_addra;
  output secret_clka /* synthesis syn_isclock = 1 */;
  output secret_rsta;
  output image_enb;
  output [15:0]image_wrdatab;
  output [3:0]image_web;
  output [15:0]image_addrb;
  output image_clkb /* synthesis syn_isclock = 1 */;
  output image_rstb;
  output secret_enb;
  output [15:0]secret_wrdatab;
  output [3:0]secret_web;
  output [15:0]secret_addrb;
  output secret_clkb /* synthesis syn_isclock = 1 */;
  output secret_rstb;
endmodule
