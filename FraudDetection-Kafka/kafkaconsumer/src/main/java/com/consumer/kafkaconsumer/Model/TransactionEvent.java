package com.consumer.kafkaconsumer.Model;
import lombok.Data;


@Data
public class TransactionEvent {
    private String transactionId;
    private String accountId;
    private double amount;
    private String timestamp;

    public String getAccountId(){
        return this.accountId;
    }

    public void setTimestamp(String timestamp){
        this.timestamp = timestamp;
    }
    
}
