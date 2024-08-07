// example.mq4

// MT4 Example EA
#property strict

input int MovingAveragePeriod = 14;

void OnTick() {
    double ma = iMA(NULL, 0, MovingAveragePeriod, 0, MODE_SMA, PRICE_CLOSE, 0);
    if (Bid > ma) {
        if (OrderSend(Symbol(), OP_BUY, 0.1, Ask, 2, 0, 0, "", 0, 0, clrBlue) < 0) {
            Print("Error: ", GetLastError());
        }
    }
}
