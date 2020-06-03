package com.isolation.icebreakers.domain;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.*;

@Entity
@Table(name = "user", schema = "icebreakers")
public class DAOUser {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;
    @Column
    private String username;
    
    @Column
    @JsonIgnore
    private String password;
    
    @Column
    private String[] traits;

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String[] getTraits() {
      return traits;
    }

    public void setTraits(String[] traits) {
      this.traits = traits;
    }

}