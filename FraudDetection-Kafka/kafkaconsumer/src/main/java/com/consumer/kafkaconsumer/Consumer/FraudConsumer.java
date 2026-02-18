package com.consumer.kafkaconsumer.Consumer;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Component;

import com.consumer.kafkaconsumer.Model.TransactionEvent;
import com.consumer.kafkaconsumer.Service.FraudService;

@Component
public class FraudConsumer {
    private final FraudService fraudService;

    public FraudConsumer(FraudService fraudService) {
        this.fraudService = fraudService;
    }

    // Method to consume messages from the "transactions" topic
    // springboot polls the topic and when a message is received, it calls this method with the message payload (TransactionEvent) and an Acknowledgment object
    // The Acknowledgment parameter allows us to manually acknowledge the message after processing
    @KafkaListener(topics = "transactions")
    public void consumer(TransactionEvent event, Acknowledgment acknowledgment) {
        System.out.println("Received transaction: " + event);
        fraudService.process(event);
        acknowledgment.acknowledge(); // Acknowledge the message
    }
}
