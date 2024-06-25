`timescale 1ns / 1ps

module tb_steganography;

    // Parameters
    localparam CLK_PERIOD = 10; // Adjust the clock period as needed

    // Signals
    reg sys_clk;
    wire ps_enb;
    reg [15:0] control_signal;
    reg [15:0] picture_size;
    reg [15:0] message_size;
    wire [15:0] respond_signal;
    wire image_ena;
    reg [7:0] image_rddataa;
    wire [3:0] image_wea;
    wire [15:0] image_addra;
    wire image_clka;
    wire image_rsta;
    wire secret_ena;
    reg [7:0] secret_rddataa;
    wire [3:0] secret_wea;
    wire [15:0] secret_addra;
    wire secret_clka;
    wire secret_rsta;
    wire image_enb;
    wire [7:0] image_wrdatab;
    wire [3:0] image_web;
    wire [15:0] image_addrb;
    wire image_clkb;
    wire image_rstb;
    wire secret_enb;
    wire [7:0] secret_wrdatab;
    wire [3:0] secret_web;
    wire [15:0] secret_addrb;
    wire secret_clkb;
    wire secret_rstb;

    // Instantiate steganography module
    steganography #(16, 16, 4, 16, 8) uut (
        .sys_clk(sys_clk),
        .ps_enb(ps_enb),
        .debug_data1(),
        .debug_data2(),
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

    // Clock generation
    always begin
        #(CLK_PERIOD/2) sys_clk = ~sys_clk;
    end

    // Initial stimulus
    initial begin
        sys_clk = 0;
        control_signal = 16'b0;
        picture_size = 16'b0;
        message_size = 16'b0;
        image_rddataa = 8'b0;
        secret_rddataa = 8'b0;
        

        // Display outputs every cycle
        $monitor("Time=%0t sys_clk=%b ps_enb=%b control_signal=%h picture_size=%h message_size=%h respond_signal=%h",
            $time, sys_clk, ps_enb, control_signal, picture_size, message_size, respond_signal);

        // Simulate for a specific duration
        #500 $stop;
    end

endmodule
