`timescale 1ns/100ps
module cordic #(parameter DATA_WIDTH = 16 , ADDR_WIDTH = 4)
(
	input  clk,rst,en,
	output done,
	input  signed [DATA_WIDTH-1:0] z,
	output signed [DATA_WIDTH-1:0] x,y
);

	wire [ADDR_WIDTH-1:0] rom_addr;
	wire [DATA_WIDTH-1:0] rom_data;

	cordic_core #(.DATA_WIDTH(DATA_WIDTH),.ADDR_WIDTH(ADDR_WIDTH)) u_cordic_core
	(
		.clk(clk),
		.rst(rst),
		.en(en),
		.done(done), 
		.z(z),
		.addr(rom_addr),
		.q(rom_data),
		.x(x),
		.y(y)
	);

	rom #(.DATA_WIDTH(DATA_WIDTH),.ADDR_WIDTH(ADDR_WIDTH)) u_rom
	(
		.addr(rom_addr),
		.q(rom_data)
	);

endmodule
