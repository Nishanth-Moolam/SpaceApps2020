package com.isolation.icebreakers.service;

import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import com.isolation.icebreakers.domain.DAOUser;
import com.isolation.icebreakers.model.PersonalityTraitsRequest;
import com.isolation.icebreakers.model.UserVO;
import com.isolation.icebreakers.repositories.UserRepository;

@Service
public class JwtUserDetailsService implements UserDetailsService {
    
    @Autowired
    private UserRepository userDao;

    @Autowired
    private PasswordEncoder bcryptEncoder;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        DAOUser user = userDao.findByUsername(username);
        if (user == null) {
            throw new UsernameNotFoundException("User not found with username: " + username);
        }
        return new org.springframework.security.core.userdetails.User(user.getUsername(), 
            user.getPassword(), new ArrayList<>());
    }
    
    public DAOUser save(UserVO user) {
        DAOUser newUser = new DAOUser();
        newUser.setUsername(user.getUsername());
        newUser.setPassword(bcryptEncoder.encode(user.getPassword()));
        return userDao.save(newUser);
    }

    public void addPersonalityTraits(String username, PersonalityTraitsRequest ptr) {
      DAOUser user = userDao.findByUsername(username);
      if (user == null) {
          throw new UsernameNotFoundException("User not found with username: " + username);
      }

      for(String s: ptr.getTraits()) {
        user.setTraits(ptr.getTraits());
      }
      
      userDao.save(user);
    }
}