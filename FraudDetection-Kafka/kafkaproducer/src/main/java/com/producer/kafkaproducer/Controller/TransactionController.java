package com.producer.kafkaproducer.Controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.producer.kafkaproducer.service.TransactionProducer;
import com.producer.kafkaproducer.model.TransactionEvent;

@RestController
@RequestMapping("/api")
public class TransactionController {
    private final TransactionProducer transactionProducer;
    // Constructor injection for TransactionProducer
    public TransactionController(TransactionProducer transactionProducer) {
        this.transactionProducer = transactionProducer;
    }

    // Endpoint to publish a transaction event
    @PostMapping("/transactions")
    public ResponseEntity<String> publishTransaction(@RequestBody TransactionEvent event) {
        event.setTimestamp(String.valueOf(System.currentTimeMillis()));
        transactionProducer.publish(event);
        return ResponseEntity.ok("Transaction published");
    }
}
