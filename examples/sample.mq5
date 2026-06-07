// sample.mq4 — MT4 Example EA


input int MovingAveragePeriod = 14;

void OnTick() {
    int ma_handle = iMA(_Symbol, PERIOD_CURRENT, MovingAveragePeriod, 0, MODE_SMA, PRICE_CLOSE);
    double ma[];
    ArraySetAsSeries(ma, true);
    if (CopyBuffer(ma_handle, 0, 0, 1, ma) <= 0) return;
    if (SymbolInfoDouble(Symbol(), SYMBOL_BID) > ma[0]) {
        if (OrderSend(Symbol(), ORDER_TYPE_BUY, 0.1, SymbolInfoDouble(Symbol(), SYMBOL_ASK), 2, 0, 0, "", 0, 0, clrBlue) < 0) {
            Print("Error: ", GetLastError());
        }
    }
}
