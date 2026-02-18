package com.consumer.kafkaconsumer.Service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import com.consumer.kafkaconsumer.Model.TransactionEvent;


@Service
public class FraudService {
    
    private int threshold; 
    private int windowMs;

    private final StringRedisTemplate redisTemplate;
    private final KafkaTemplate<String, String> kafkaTemplate;


    public FraudService(StringRedisTemplate redisTemplate, KafkaTemplate<String, String> kafkaTemplate, @Value("${fraud.threshold}") int threshold,
            @Value("${fraud.window-ms}") int windowMs) {
        this.redisTemplate = redisTemplate;
        this.kafkaTemplate = kafkaTemplate;
        this.threshold = threshold;
        this.windowMs = windowMs;
    }

    public void process(TransactionEvent event) {
       String redisKey = "fraud:user" + event.getAccountId();
       long now = System.currentTimeMillis();
       long windowStart = now - this.windowMs; // 1 minute window

       // add the current transaction timestamp to the sorted set
       redisTemplate.opsForZSet().add(redisKey, String.valueOf(now), now);
       // 
       redisTemplate.opsForZSet().removeRangeByScore(redisKey, 0, windowStart);
       Long count = redisTemplate.opsForZSet().zCard(redisKey);

       if (count != null && count > this.threshold) {
           System.out.println("Fraud detected for account: " + event.getAccountId());
           kafkaTemplate.send("fraud-alerts", event.getAccountId(), "Fraud alerts detected for account: " + event.getAccountId());
       }
    
    }
}
