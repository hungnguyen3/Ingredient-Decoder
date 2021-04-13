module top(
    input logic CLOCK_50, input logic [3:0] KEY, output logic done
);
    logic start_cropping, start_header = 0;
    logic doneValue = 0;
    logic done_cropping;
    logic done_header;
        logic start_bb;
    logic done_bb;

        logic[15:0] rddata_bb;
    logic[31:0] addr_bb;

    // mem for 100x100 pictures
    logic [7:0] readMem [29999:0];
    logic [7:0] writeMem [29999:0];

    // instantiate boundingbox
    logic[31:0] readaddr;
    logic[15:0] readdata;
    logic[31:0] writeAddr;
    logic[15:0] wrdata;
    logic wrenCrop;    
    logic[10:0] xMin;
    logic[10:0] yMin;
    logic[10:0] xMax;
    logic[10:0] yMax;
    cropping cropping(.clk(CLOCK_50), .rst_n(KEY[3]), .start(start_cropping), .done(done_cropping),
                                .readAddr(readaddr), .readdata(readdata),
                                .writeAddr(writeAddr), .wrdata(wrdata), .wren(wrenCrop),
                                .xMin(xMin), .xMax(xMax), .yMin(yMin), .yMax(yMax));

    logic [23:0] headerAddr;
    logic wrenHeader;
    logic [15:0] wrdata_header;

     boundingBox boundingBox(.clk(CLOCK_50), .rst_n(KEY[3]), .start(start_bb), .done(done_bb),
                                .rddata(rddata_bb), .addr(addr_bb),
                                .xMin(xMin), .xMax(xMax),
                                .yMin(yMin), .yMax(yMax));

    header header(.clk(CLOCK_50), .rst_n(KEY[3]),
                        .start(start_header), .done(done_header),
                        .addr(headerAddr), .wren(wrenHeader), .wrdata(wrdata_header),
                        .xMin(xMin), .xMax(xMax),
                        .yMin(yMin), .yMax(yMax));

    enum {init, process_bb, process_header, process_cropping, finished} state = init;

    assign done = doneValue;

    always@(posedge CLOCK_50) begin
        if(~KEY[3]) begin
            state <= init;
            doneValue <= 0;
        end
        else begin
            doneValue <= 0;
            case(state)
                init: begin
                    start_header <= 0; // start processing header
                    start_cropping <= 0;
                    start_bb <= 1;
                    state <= process_bb;
                end
                process_bb: begin
                    start_bb <= 0;
                    rddata_bb <= readMem[addr_bb]; // pass rddata to boundingBox
                    if(done_bb) begin
                        start_header <= 1;
                        state <= process_header;
                    end
                    else begin
                        state <= process_bb;
                    end
                end
                process_header: begin
                    start_header <= 0; // deassert start_header
                    if(wrenHeader)
                    begin
                        writeMem[headerAddr] <= wrdata_header;
                    end
                    if(done_header) begin
                        start_cropping <= 1;
                        state <= process_cropping;
                    end
                    else begin
                        state <= process_header;
                    end
                end
                process_cropping: 
                begin
                    start_cropping <= 0; // deassert start_cropping
                    readdata <= readMem[readaddr];
                    if(wrenCrop)
                    begin
                        writeMem[writeAddr] <= wrdata;
                    end
                    if(done_cropping) begin
                        state <= finished;
                    end
                    else begin
                        state <= process_cropping;
                    end
                end
                finished: begin
                    state <= finished;
                    doneValue <= 1;
                end
            endcase
        end
    end
endmodule