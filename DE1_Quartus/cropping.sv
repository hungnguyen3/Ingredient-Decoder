//rddata: only one of RGB
//readaddr: where in the hex file to read the original data 
//readdata: the data being read
//writeaddr: where to write the cropped file
//wrdata: the data to write (the RGB inside the cropped area)
//wren: write enable
//xMin, xMax: the samllest and lagrest x coordinates for where the image is not the background colour. Start at the R position of the pixel
//yMin, yMax: the samllest and lagrest y coordinates for where the image is not the background colour. Start at the R position of the pixel
//start/done: on reset, done = 0. when start = 1, we drop done and start processing. After processing, done is raised. We restart when start is reasserted. done indicates valid data.
//PARAMETERS: Hardware catures fixed dimensions bmp
module cropping 
#(
    parameter WIDTH = 100, 					// Image width
	HEIGHT 	= 100 						    // Image height
)
(
    input logic clk, input logic rst_n,
    input logic start, output logic done,
    output logic [31:0] readAddr, input logic [15:0] readdata,
    output logic [31:0] writeAddr, output logic [15:0] wrdata, output logic wren,
    input logic[10:0] xMin, input logic[10:0] xMax,
    input logic[10:0] yMin, input logic[10:0] yMax
);

    logic doneValue = 0;
    logic [31:0] readAddrValue;
    logic [31:0] writeAddrValue = 54;
    logic wrenValue = 0;
    logic [15:0] wrdataValue = 0;


    assign done = doneValue;
    assign readAddr = readAddrValue;
    assign wren = wrenValue;
    assign wrdata = wrdataValue;

    logic [10:0] xPos;
    logic [10:0] yPos;
    logic [1:0] rgb = 0;
    logic [1:0] paddingCounter = 0;

    assign writeAddr = writeAddrValue;

    //read memory, write it, maybe add cropping
    enum {init, readMem, writeMem, padding, finished} state = init;

    assign readAddrValue = (yPos - yMin + (HEIGHT - yMax - 1)) * WIDTH * 3 + xPos * 3 + (3-rgb-1);

    always@(posedge clk)
    begin
        if (!rst_n)
        begin
            xPos <= xMin;
            yPos <= yMin;
            rgb <= 0;
            paddingCounter <= 0;
            state <= init;
            writeAddrValue <= 54;
        end

        else
        begin
            case (state)
                init:
                begin
                    if(start) // start the process when start is asserted
                    begin
                        xPos <= xMin;
                        yPos <= yMin;
                        rgb <= 0;
                        paddingCounter <= 0;
                        writeAddrValue <= 54;
                        state <= readMem;
                    end
                    else 
                    begin
                        state <= init;
                    end
                end

                readMem:
                begin
                    state <= writeMem;
                end

                writeMem:
                begin
                    writeAddrValue <= writeAddrValue + 1;
                    if(rgb + 1 < 3)
                    begin
                        rgb <= rgb + 1;
                        state <= readMem;
                    end

                    else
                    begin
                        rgb <= 0;
                        if(xPos + 1 <= xMax)
                        begin
                            xPos <= xPos + 1;
                            state <= readMem;
                        end
                        else 
                        begin
                            if(((3*(xPos - xMin + 1) + paddingCounter) & 3) != 0) //if current xPos + amount of padding mod 3 is not 0
                            begin
                                state <= padding;
                            end
                            else
                            begin
                                xPos <= xMin;
                                if(yPos + 1 <= yMax)
                                begin
                                    yPos <= yPos + 1;
                                    state <= readMem;
                                end
                                else
                                begin
                                    xPos <= xMin;
                                    yPos <= yMin;
                                    rgb <= 0;
                                    paddingCounter <= 0; //finish padding, reset counter
                                    state <= finished;
                                end
                            end
                        end
                    end
                end

                padding:
                begin
                    writeAddrValue <= writeAddrValue + 1;

                    // check multiple of 4
                    if(((3*(xPos - xMin + 1) + paddingCounter + 1) & 3) != 0) //if current xPos + amount of padding mod 3 is not 0
                    begin
                        state <= padding;
                        paddingCounter <= paddingCounter + 1;
                    end
                    else
                    begin
                        xPos <= xMin;
                        if(yPos + 1 <= yMax)
                        begin
                            yPos <= yPos + 1;
                            state <= readMem;
                            paddingCounter <= 0; //finish padding, reset counter    
                        end
                        else
                        begin
                            xPos <= xMin;
                            yPos <= yMin;
                            rgb <= 0;
                            paddingCounter <= 0; //finish padding, reset counter
                            state <= finished;
                        end
                    end
                end

                finished:
                begin
                    if(start)
                    begin
                        xPos <= xMin;
                        yPos <= yMin;
                        rgb <= 0;
                        state <= readMem;
                        writeAddrValue <= 54;
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
        case (state)
            init:
            begin
                doneValue = 0;
                wrenValue = 0;
                wrdataValue = 0;
            end

            readMem:
            begin
                doneValue = 0;
                wrenValue = 0;
                wrdataValue = 0;
            end

            writeMem:
            begin
                doneValue = 0;
                wrenValue = 1;
                wrdataValue = readdata;
            end

            padding:
            begin
                doneValue = 0;
                wrenValue = 1;
                wrdataValue = 0;
            end

            finished:
            begin
                doneValue = 1;
                wrenValue = 0;
                wrdataValue = 0;
            end
        endcase
        
    end

endmodule