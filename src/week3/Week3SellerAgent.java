package week3;

import jade.core.Agent;
import jade.core.behaviours.*;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;

import java.util.*;

/**
 * Week 3 Lab: Book Seller Agent
 * 
 * Seller agent that:
 * 1. Registers with Directory Facilitator (DF)
 * 2. Responds to CFP with price proposals
 * 3. Processes purchase orders
 */
public class Week3SellerAgent extends Agent {
    
    // Book catalogue: title -> price
    private Map<String, Integer> catalogue = new HashMap<>();
    
    @Override
    protected void setup() {
        System.out.println("\n===========================================");
        System.out.println("       WEEK 3 LAB: Book Seller Agent       ");
        System.out.println("===========================================");
        System.out.println("[Seller] " + getAID().getLocalName() + " started.");
        
        // Initialize catalogue with some books
        catalogue.put("Java-Programming", 50);
        catalogue.put("JADE-Tutorial", 35);
        catalogue.put("AI-Agents", 75);
        catalogue.put("Multi-Agent-Systems", 60);
        
        System.out.println("\n[Catalogue]");
        for (Map.Entry<String, Integer> entry : catalogue.entrySet()) {
            System.out.println("  - " + entry.getKey() + ": $" + entry.getValue());
        }
        
        // Register with Directory Facilitator
        registerWithDF();
        
        // Add behaviours
        addBehaviour(new OfferRequestHandler());
        addBehaviour(new PurchaseOrderHandler());
        
        System.out.println("\n[Ready] Waiting for buyer requests...\n");
    }
    
    /**
     * Register this seller with the DF
     */
    private void registerWithDF() {
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());
        
        ServiceDescription sd = new ServiceDescription();
        sd.setType("book-selling");
        sd.setName("book-trading");
        dfd.addServices(sd);
        
        try {
            DFService.register(this, dfd);
            System.out.println("[DF] Registered as book seller.");
        } catch (FIPAException e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Handle CFP (Call For Proposal) messages
     */
    private class OfferRequestHandler extends CyclicBehaviour {
        @Override
        public void action() {
            MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.CFP);
            ACLMessage msg = receive(mt);
            
            if (msg != null) {
                String bookTitle = msg.getContent();
                System.out.println("[CFP Received] Looking for: " + bookTitle);
                
                ACLMessage reply = msg.createReply();
                
                if (catalogue.containsKey(bookTitle)) {
                    int price = catalogue.get(bookTitle);
                    reply.setPerformative(ACLMessage.PROPOSE);
                    reply.setContent(String.valueOf(price));
                    System.out.println("[Proposing] $" + price + " for " + bookTitle);
                } else {
                    reply.setPerformative(ACLMessage.REFUSE);
                    reply.setContent("not-available");
                    System.out.println("[Refusing] Book not in catalogue");
                }
                
                send(reply);
            } else {
                block();
            }
        }
    }
    
    /**
     * Handle ACCEPT_PROPOSAL messages (purchase orders)
     */
    private class PurchaseOrderHandler extends CyclicBehaviour {
        @Override
        public void action() {
            MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.ACCEPT_PROPOSAL);
            ACLMessage msg = receive(mt);
            
            if (msg != null) {
                String bookTitle = msg.getContent();
                System.out.println("\n[Order Received] " + bookTitle);
                
                ACLMessage reply = msg.createReply();
                
                if (catalogue.containsKey(bookTitle)) {
                    int price = catalogue.get(bookTitle);
                    catalogue.remove(bookTitle); // Sell the book
                    
                    reply.setPerformative(ACLMessage.INFORM);
                    reply.setContent("sold");
                    
                    System.out.println("[SOLD] '" + bookTitle + "' for $" + price);
                    System.out.println("  To: " + msg.getSender().getLocalName());
                } else {
                    reply.setPerformative(ACLMessage.FAILURE);
                    reply.setContent("not-available");
                    System.out.println("[Failed] Book no longer available");
                }
                
                send(reply);
            } else {
                block();
            }
        }
    }
    
    @Override
    protected void takeDown() {
        // Deregister from DF
        try {
            DFService.deregister(this);
            System.out.println("[DF] Deregistered from directory.");
        } catch (FIPAException e) {
            e.printStackTrace();
        }
        System.out.println("[Seller] " + getAID().getLocalName() + " terminated.\n");
    }
}
