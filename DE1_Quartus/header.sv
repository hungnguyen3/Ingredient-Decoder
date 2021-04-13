module header 
#(parameter WIDTH 	= 100,							// Image width
			HEIGHT 	= 100							// Image height
)
(
    input logic clk, input logic rst_n,
    input logic start, output logic done,
    output logic [23:0] addr, output logic wren, output logic [15:0] wrdata,
    input logic[10:0] xMin, input logic[10:0] xMax,
    input logic[10:0] yMin, input logic[10:0] yMax
);

    logic doneValue = 0;
    logic [23:0] addrValue = 0;
    logic wrenValue = 0;
    logic [15:0] wrdataValue = 0;

    assign done = doneValue;
    assign addr = addrValue;
    assign wren = wrenValue;
    assign wrdata = wrdataValue;

    integer BMP_header [0 : 53];	

    logic [31:0] area;

    logic [23:0] nonPaddedWidth;
    logic [23:0] modFourZero;
    logic [23:0] modFourOne;
    logic [23:0] modFourTwo;
    logic [23:0] modFourThree;
    logic [23:0] paddedWidth;


    assign nonPaddedWidth = 3*(xMax - xMin + 1);
    assign modFourZero = ((nonPaddedWidth & 3) == 0)? nonPaddedWidth : 0;
    assign modFourOne = (((nonPaddedWidth + 1) & 3) == 0)? (nonPaddedWidth + 1) : 0;
    assign modFourTwo = (((nonPaddedWidth + 2) & 3) == 0)? (nonPaddedWidth + 2) : 0;
    assign modFourThree = (((nonPaddedWidth + 3) & 3) == 0)? (nonPaddedWidth + 3) : 0;
    assign paddedWidth = (modFourZero!=0) ? modFourZero : (modFourOne!=0) ? modFourOne : (modFourTwo!=0) ? modFourTwo : (modFourThree!=0) ? modFourThree : 0;
    assign area = paddedWidth * (yMax - yMin + 1);

    assign BMP_header[0] = 66; //B
    assign BMP_header[1] = 77; //M

    // correct!
    assign BMP_header[2] = area+54 - (area>>8) * 16 * 16;
    assign BMP_header[3] = (area+54>>8) - (area>>16) * 16 *16;
    assign BMP_header[4] = (area+54>>16) - (area>>24) * 16 * 16;
    assign BMP_header[5] = (area+54>>24) - (area>>32) * 16 * 16;
        
    assign BMP_header[6] = 0;
    assign BMP_header[7] = 0;
    assign BMP_header[8] = 0;
    assign BMP_header[9] = 0;

    assign BMP_header[10] = 54;
	assign BMP_header[11] =  0;
	assign BMP_header[12] =  0;
	assign BMP_header[13] =  0;
	assign BMP_header[14] = 40;
	assign BMP_header[15] =  0;
	assign BMP_header[16] =  0;
	assign BMP_header[17] =  0;
    
    assign BMP_header[18] = (xMax - xMin + 1) - ((xMax - xMin + 1)>>8) * 16 * 16;
    assign BMP_header[19] = ((xMax - xMin + 1)>>8) - ((xMax - xMin + 1)>>16) * 16 *16;
    assign BMP_header[20] = ((xMax - xMin + 1)>>16) - ((xMax - xMin + 1)>>24) * 16 * 16;
    assign BMP_header[21] = ((xMax - xMin + 1)>>24) - ((xMax - xMin + 1)>>32) * 16 * 16;

    assign BMP_header[22] = (yMax - yMin + 1) - ((yMax - yMin + 1)>>8) * 16 * 16;
    assign BMP_header[23] = ((yMax - yMin + 1)>>8) - ((yMax - yMin + 1)>>16) * 16 *16;
    assign BMP_header[24] = ((yMax - yMin + 1)>>16) - ((yMax - yMin + 1)>>24) * 16 * 16;
    assign BMP_header[25] = ((yMax - yMin + 1)>>24) - ((yMax - yMin + 1)>>32) * 16 * 16;

    assign BMP_header[26] = 1;
    assign BMP_header[27] = 0;

    assign BMP_header[28] = 24;
    assign BMP_header[29] = 0;

    assign BMP_header[30] = 0;
    assign BMP_header[31] = 0;
    assign BMP_header[32] = 0;
    assign BMP_header[33] = 0;

    assign BMP_header[34] = area - (area>>8) * 16 * 16;
    assign BMP_header[35] = (area>>8) - (area>>16) * 16 *16;
    assign BMP_header[36] = (area>>16) - (area>>24) * 16 * 16;
    assign BMP_header[37] = (area>>24) - (area>>32) * 16 * 16;

    assign BMP_header[38] = 0;
    assign BMP_header[39] = 0;
    assign BMP_header[40] = 0;
    assign BMP_header[41] = 0;

    assign BMP_header[42] = 0;
    assign BMP_header[43] = 0;
    assign BMP_header[44] = 0;
    assign BMP_header[45] = 0;

    assign BMP_header[46] = 0;
    assign BMP_header[47] = 0;
    assign BMP_header[48] = 0;
    assign BMP_header[49] = 0;

    assign BMP_header[50] = 0;
    assign BMP_header[51] = 0;
    assign BMP_header[52] = 0;
    assign BMP_header[53] = 0;

    enum {init, writing, finished} state = init;
    integer i = 0;

    always@(posedge clk)
    begin
        if (!rst_n)
        begin
            i <= 0;
            state <= init;
        end

        else
        begin
            case (state)
                init:
                begin
                    if(start) // start the process when start is asserted
                    begin
                        i <= 0;
                        state <= writing;
                    end
                    else 
                    begin
                        state <= init;
                    end
                end

                writing:
                begin
                    if(i + 1 < 54)
                    begin
                        i <= i + 1;
                        state <= writing;
                    end
                    else
                    begin
                        state <= finished;
                    end
                end

                finished:
                begin
                    if(start)
                    begin
                        i <= 0;
                        state <= writing;
                    end
                    else
                    begin
                        state <= finished;
                    end
                end
            endcase
        end
    end

    always @(*)
    begin
        doneValue = 0;
        case(state) 
            init:
            begin
                addrValue = 0;
                wrenValue = 0;
                wrdataValue = 0;
            end

            writing:
            begin
                addrValue = i;
                wrenValue = 1;
                wrdataValue = BMP_header[i];
            end

            finished:
            begin
                doneValue = 1;
                wrenValue = 0;
                wrdataValue = 0;
                addrValue = 0;
            end
        endcase
    end
endmodule
