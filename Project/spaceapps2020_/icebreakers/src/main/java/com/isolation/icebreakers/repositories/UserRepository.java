package com.isolation.icebreakers.repositories;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import com.isolation.icebreakers.domain.DAOUser;

@Repository
public interface UserRepository extends CrudRepository<DAOUser, Integer> {
    
    DAOUser findByUsername(String username);
    
}