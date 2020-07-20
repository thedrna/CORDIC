module CORDIC #(parameter data_width = 16, address_width = 4, mode = 0)
  (input clk, reset, enable,
   input signed [data_width-1:0] z, delta_z,
   output [address_width-1:0] address,
   output signed [data_width-1:0] x, y,
   output done
  );
  
  reg state, nxt_state, done_reg;
  
  parameter idle = 1'b0, calculation = 1'b1;
  
  reg [address_width-1:0] step, nxt_step;
  
  reg signed [data_width-1:0]x_reg,y_reg,x_next,y_next,z_reg,z_next;
  
  always @ (posedge clk, posedge reset) 
	begin
		if (reset)
		  begin
			 state <= idle;
			 step <= 0;
			 x_reg <= 0;
			 y_reg <= 0;
			 z_reg <= 0;
			 done_reg <= 0;
		  end
	 else
		begin
			state <= nxt_state;
			step <= nxt_step;
			x_reg <= x_next;
			y_reg <= y_next;
			z_reg <= z_next;
		end	
	end
	
	always @ (*)
	 begin
		nxt_step = step;
		case (state)
			idle:
			 begin
				if (enable)
				  begin
					 nxt_state = calcuation;
				  end
				else
				 begin
					 nxt_state = idle;
				 end
				nxt_step = 0;
			end
			calculation:
			 begin
				if (step == (data_width-2))
				begin
					nxt_state = idle;
					done_reg = 1'b1;
				end
				else
				  begin
					  nxt_step = step + 1'b1;
					  nxt_state = calcualtion;
				  end
			end
		endcase
	end


  always @ (*)
	begin
		case (state)
			idle:
			begin
			  case (mode)
			  begin
			      0:
			         x_next = x;
			      1:
			         x_next = 0.6073;
			      2:
			         x_next = 1.2075;
			  endcase
				y_next = 0;
				z_next = z;
			end
			
			calculation:
			begin
			     if (mode!=0)
			       begin
			         if (z_reg[data_width-1]==1'b0)//check polarity
				          begin
					         x_next = x_reg - (y_reg >>> step);
					         y_next = y_reg + (x_reg >>> step);
					         z_next = z_reg - delta_z;
				          end
				       else
				          begin
					         x_next = x_reg + (y_reg >>> step);
					         y_next = y_reg - (x_reg >>> step);
					         z_next = z_reg + delta_z;
				          end
				     end
				     
				     else
				     begin
				     end
				     
				    end
			     end
	       endcase
	     end
	     
			  
			  
			    
			
  assign address = step;
  assign x = done? x_reg: 0;
  assign y = done? y_reg: 0;
  assign done = done_reg;
endmodule