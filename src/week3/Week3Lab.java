package week3;

import jade.core.Agent;
import jade.core.AID;
import jade.core.behaviours.*;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;

import java.util.*;

/**
 * Week 3 Lab: Book Trading Multi-Agent System
 * 
 * This is a simplified buyer agent that demonstrates:
 * 1. Directory Facilitator (DF) service registration/search
 * 2. Contract Net Protocol (CFP, PROPOSE, ACCEPT_PROPOSAL)
 * 3. Multi-step negotiation behaviour
 * 
 * To run (requires seller agents running first):
 *   1. Start seller: java -cp lib/jade.jar;bin jade.Boot -gui -agents "seller1:week3.Week3SellerAgent"
 *   2. Start buyer: java -cp lib/jade.jar;bin jade.Boot -container -agents "buyer:week3.Week3Lab(Java-Programming)"
 */
public class Week3Lab extends Agent {
    
    private String targetBookTitle;
    private AID[] sellerAgents;
    
    @Override
    protected void setup() {
        System.out.println("\n===========================================");
        System.out.println("      WEEK 3 LAB: Book Trading System      ");
        System.out.println("===========================================");
        System.out.println("[Buyer Agent] " + getAID().getLocalName() + " started.");
        
        // Get book title from arguments
        Object[] args = getArguments();
        if (args != null && args.length > 0) {
            targetBookTitle = (String) args[0];
            System.out.println("[Target Book] " + targetBookTitle);
            
            // Search for sellers every 5 seconds
            addBehaviour(new TickerBehaviour(this, 5000) {
                @Override
                protected void onTick() {
                    searchForSellers();
                }
            });
        } else {
            System.out.println("[ERROR] No book title specified!");
            System.out.println("  Usage: buyer:week3.Week3Lab(book-title)");
            doDelete();
        }
    }
    
    /**
     * Search DF for registered book sellers
     */
    private void searchForSellers() {
        System.out.println("\n[Searching] Looking for book sellers...");
        
        DFAgentDescription template = new DFAgentDescription();
        ServiceDescription sd = new ServiceDescription();
        sd.setType("book-selling");
        template.addServices(sd);
        
        try {
            DFAgentDescription[] results = DFService.search(this, template);
            
            if (results.length > 0) {
                sellerAgents = new AID[results.length];
                System.out.println("[Found] " + results.length + " seller(s):");
                
                for (int i = 0; i < results.length; i++) {
                    sellerAgents[i] = results[i].getName();
                    System.out.println("  - " + sellerAgents[i].getLocalName());
                }
                
                // Start negotiation
                addBehaviour(new BookNegotiator());
            } else {
                System.out.println("[Waiting] No sellers found yet...");
            }
        } catch (FIPAException e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Behaviour for negotiating book purchases
     */
    private class BookNegotiator extends Behaviour {
        private AID bestSeller;
        private int bestPrice = Integer.MAX_VALUE;
        private int repliesCnt = 0;
        private MessageTemplate mt;
        private int step = 0;
        
        @Override
        public void action() {
            switch (step) {
                case 0: // Send CFP to all sellers
                    System.out.println("\n[Step 1] Sending CFP for '" + targetBookTitle + "'");
                    
                    ACLMessage cfp = new ACLMessage(ACLMessage.CFP);
                    for (AID seller : sellerAgents) {
                        cfp.addReceiver(seller);
                    }
                    cfp.setContent(targetBookTitle);
                    cfp.setConversationId("book-trade-" + System.currentTimeMillis());
                    cfp.setReplyWith("cfp-" + System.currentTimeMillis());
                    send(cfp);
                    
                    mt = MessageTemplate.and(
                        MessageTemplate.MatchConversationId(cfp.getConversationId()),
                        MessageTemplate.MatchInReplyTo(cfp.getReplyWith())
                    );
                    step = 1;
                    break;
                    
                case 1: // Collect proposals
                    ACLMessage reply = receive(mt);
                    if (reply != null) {
                        if (reply.getPerformative() == ACLMessage.PROPOSE) {
                            int price = Integer.parseInt(reply.getContent());
                            System.out.println("[Proposal] " + reply.getSender().getLocalName() + 
                                             " offers $" + price);
                            
                            if (price < bestPrice) {
                                bestPrice = price;
                                bestSeller = reply.getSender();
                            }
                        } else if (reply.getPerformative() == ACLMessage.REFUSE) {
                            System.out.println("[Refused] " + reply.getSender().getLocalName() + 
                                             " - book not available");
                        }
                        
                        repliesCnt++;
                        if (repliesCnt >= sellerAgents.length) {
                            step = 2;
                        }
                    } else {
                        block();
                    }
                    break;
                    
                case 2: // Accept best proposal
                    if (bestSeller != null) {
                        System.out.println("\n[Step 2] Accepting offer from " + 
                                         bestSeller.getLocalName() + " at $" + bestPrice);
                        
                        ACLMessage order = new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);
                        order.addReceiver(bestSeller);
                        order.setContent(targetBookTitle);
                        order.setConversationId("purchase-" + System.currentTimeMillis());
                        order.setReplyWith("order-" + System.currentTimeMillis());
                        send(order);
                        
                        mt = MessageTemplate.MatchInReplyTo(order.getReplyWith());
                        step = 3;
                    } else {
                        System.out.println("\n[Failed] No sellers have '" + targetBookTitle + "'");
                        step = 4;
                    }
                    break;
                    
                case 3: // Receive confirmation
                    reply = receive(mt);
                    if (reply != null) {
                        if (reply.getPerformative() == ACLMessage.INFORM) {
                            System.out.println("\n===========================================");
                            System.out.println("[SUCCESS] Purchased '" + targetBookTitle + "'");
                            System.out.println("  From: " + bestSeller.getLocalName());
                            System.out.println("  Price: $" + bestPrice);
                            System.out.println("===========================================\n");
                            myAgent.doDelete();
                        } else {
                            System.out.println("[Failed] Book already sold!");
                        }
                        step = 4;
                    } else {
                        block();
                    }
                    break;
            }
        }
        
        @Override
        public boolean done() {
            return step == 4;
        }
    }
    
    @Override
    protected void takeDown() {
        System.out.println("[Buyer] " + getAID().getLocalName() + " terminated.\n");
    }
}
