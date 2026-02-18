package com.producer.kafkaproducer.service;

import java.util.concurrent.CompletableFuture;

import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;

import com.producer.kafkaproducer.model.TransactionEvent;

@Service
public class TransactionProducer {
    
    private final KafkaTemplate<String, TransactionEvent> kafkaTemplate;

    public TransactionProducer(KafkaTemplate<String, TransactionEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }   

  public void publish(TransactionEvent event) {

    CompletableFuture<SendResult<String, TransactionEvent>> future =
            kafkaTemplate.send("transactions",
                    event.getAccountId(),
                    event);

    future.whenComplete((result, ex) -> {
        if (ex == null) {
            System.out.println("Sent successfully to partition "
                    + result.getRecordMetadata().partition()
                    + " offset "
                    + result.getRecordMetadata().offset());
        } else {
            System.err.println("Failed to send: " + ex.getMessage());
        }
    });
}

}
