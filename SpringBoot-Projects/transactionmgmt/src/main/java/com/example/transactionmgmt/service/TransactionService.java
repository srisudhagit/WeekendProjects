package com.example.transactionmgmt.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.transactionmgmt.exception.TransactionNotFoundException;
import com.example.transactionmgmt.model.Transaction;
import com.example.transactionmgmt.model.TransactionStatus;
import com.example.transactionmgmt.repository.TransactionRespository;

@Service
@Transactional
public class TransactionService {
    private final TransactionRespository transactionRespository;

    public TransactionService(TransactionRespository transactionRespository) {
        this.transactionRespository = transactionRespository;
    }

    public Transaction saveTransaction(Transaction transaction) {
        transaction.setStatus(TransactionStatus.PENDING);
        return transactionRespository.save(transaction);
    }

    @Transactional(readOnly = true)
    public Transaction getTransactionById(Long id) {
        return transactionRespository.findById(id).orElseThrow(() -> new TransactionNotFoundException("Transaction not found with id: " + id));
    }

    @Transactional(readOnly = true)
    public Page<Transaction> getAllTransactions(Pageable pageable) {
        return transactionRespository.findAll(pageable);
    }


    public Transaction updateTransactionStatus(Long id, TransactionStatus status) {
        Transaction transaction = getTransactionById(id);
        transaction.setStatus(status);
        return transactionRespository.save(transaction);
    }

}
