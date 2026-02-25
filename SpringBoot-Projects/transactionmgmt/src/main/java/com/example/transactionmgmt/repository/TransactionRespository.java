package com.example.transactionmgmt.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.transactionmgmt.model.Transaction;

@Repository
public interface TransactionRespository extends JpaRepository<Transaction, Long> {
    
    public Page<Transaction> findAll(Pageable pageable);
}
