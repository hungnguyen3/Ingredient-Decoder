module whiteTwo(
    input logic CLOCK_50, input logic reset_n,
    input logic rd_en, input logic wr_en,

    input logic [31:0] hex_value_index, // hex_value [39:24], hex_index [23:0]
    output logic [31:0] out // xMin stored in [31:24], xMax[23:16], yMin[15:8], yMax[7:0]
);
    parameter WIDTH = 160, HEIGHT = 90, RESET = 99999;
    logic [7:0] x;
    logic [7:0] y;
    logic [2:0] rgb;
    logic [7:0] xMin, xMax, yMin, yMax;

    always@(posedge CLOCK_50) begin
        if(~reset_n || hex_value_index[23:0] == 99999) begin // reset
            x <= 0;
            y <= HEIGHT - 1;
            rgb <= 0;
            xMin = WIDTH-1;
            xMax = 0;
            yMin = HEIGHT-1;
            yMax = 0;
        end
        else if(wr_en == 1) begin
            if(rgb != 2) begin
                rgb <= rgb + 1;
            end
            else if(rgb == 2 && x != WIDTH - 1) begin
                rgb <= 0;
                x <= x + 1;
            end
            else if(rgb == 2 && x == WIDTH -1 && y != 0) begin
                rgb <= 0;
                x <= 0;
                y <= y - 1;
            end
            else if(y == 0) begin
                y <= y;
                x <= x;
                rgb <= rgb;
            end

            if(hex_value_index[31:24] < 100) begin // update coordinate when not white
                if(x < xMin) 
                begin
                    xMin <= x;
                end
                if(x > xMax)
                begin
                    xMax <= x;
                end
                if(y < yMin)
                begin
                    yMin <= y;
                end
                if(y > yMax)
                begin
                    yMax <= y;
                end
            end
        end
    end

    assign out = {xMin, xMax, yMin, yMax}; // assign output
endmodule