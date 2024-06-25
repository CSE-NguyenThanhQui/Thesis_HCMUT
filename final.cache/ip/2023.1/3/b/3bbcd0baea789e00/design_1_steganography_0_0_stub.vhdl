-- Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
-- Copyright 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2023.1 (win64) Build 3865809 Sun May  7 15:05:29 MDT 2023
-- Date        : Sat Jan 20 15:17:26 2024
-- Host        : LAPTOP-NS7LM8D6 running 64-bit major release  (build 9200)
-- Command     : write_vhdl -force -mode synth_stub -rename_top decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix -prefix
--               decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix_ design_1_steganography_0_0_stub.vhdl
-- Design      : design_1_steganography_0_0
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xczu3eg-sbva484-1-i
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix is
  Port ( 
    sys_clk : in STD_LOGIC;
    ps_enb : out STD_LOGIC;
    debug_data1 : out STD_LOGIC_VECTOR ( 15 downto 0 );
    debug_data2 : out STD_LOGIC_VECTOR ( 15 downto 0 );
    control_signal : in STD_LOGIC_VECTOR ( 15 downto 0 );
    picture_size : in STD_LOGIC_VECTOR ( 15 downto 0 );
    message_size : in STD_LOGIC_VECTOR ( 15 downto 0 );
    respond_signal : out STD_LOGIC_VECTOR ( 15 downto 0 );
    image_ena : out STD_LOGIC;
    image_rddataa : in STD_LOGIC_VECTOR ( 15 downto 0 );
    image_wea : out STD_LOGIC_VECTOR ( 3 downto 0 );
    image_addra : out STD_LOGIC_VECTOR ( 15 downto 0 );
    image_clka : out STD_LOGIC;
    image_rsta : out STD_LOGIC;
    secret_ena : out STD_LOGIC;
    secret_rddataa : in STD_LOGIC_VECTOR ( 15 downto 0 );
    secret_wea : out STD_LOGIC_VECTOR ( 3 downto 0 );
    secret_addra : out STD_LOGIC_VECTOR ( 15 downto 0 );
    secret_clka : out STD_LOGIC;
    secret_rsta : out STD_LOGIC;
    image_enb : out STD_LOGIC;
    image_wrdatab : out STD_LOGIC_VECTOR ( 15 downto 0 );
    image_web : out STD_LOGIC_VECTOR ( 3 downto 0 );
    image_addrb : out STD_LOGIC_VECTOR ( 15 downto 0 );
    image_clkb : out STD_LOGIC;
    image_rstb : out STD_LOGIC;
    secret_enb : out STD_LOGIC;
    secret_wrdatab : out STD_LOGIC_VECTOR ( 15 downto 0 );
    secret_web : out STD_LOGIC_VECTOR ( 3 downto 0 );
    secret_addrb : out STD_LOGIC_VECTOR ( 15 downto 0 );
    secret_clkb : out STD_LOGIC;
    secret_rstb : out STD_LOGIC
  );

end decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix;

architecture stub of decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "sys_clk,ps_enb,debug_data1[15:0],debug_data2[15:0],control_signal[15:0],picture_size[15:0],message_size[15:0],respond_signal[15:0],image_ena,image_rddataa[15:0],image_wea[3:0],image_addra[15:0],image_clka,image_rsta,secret_ena,secret_rddataa[15:0],secret_wea[3:0],secret_addra[15:0],secret_clka,secret_rsta,image_enb,image_wrdatab[15:0],image_web[3:0],image_addrb[15:0],image_clkb,image_rstb,secret_enb,secret_wrdatab[15:0],secret_web[3:0],secret_addrb[15:0],secret_clkb,secret_rstb";
attribute X_CORE_INFO : string;
attribute X_CORE_INFO of stub : architecture is "steganography,Vivado 2023.1";
begin
end;
