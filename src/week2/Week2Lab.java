package week2;

import jade.core.Agent;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

/**
 * Week 2 Lab: Multi-Container Communication
 * 
 * This agent demonstrates:
 * 1. Creating agents in different containers
 * 2. Inter-agent messaging using ACLMessage
 * 3. Message templates and filtering
 * 4. CyclicBehaviour for continuous message listening
 * 
 * To run:
 *   Main Container:
 *     java -cp lib/jade.jar;bin jade.Boot -gui -platform-id Platform1 -agents "receiver:week2.Week2Lab"
 *   
 *   Peripheral Container (run in separate terminal):
 *     java -cp lib/jade.jar;bin jade.Boot -container -agents "sender:week2.Week2Lab(send,receiver)"
 */
public class Week2Lab extends Agent {
    
    private boolean isSender = false;
    private String targetAgent = null;
    
    @Override
    protected void setup() {
        System.out.println("\n===========================================");
        System.out.println("       WEEK 2 LAB: Container Communication  ");
        System.out.println("===========================================");
        
        // Get agent info
        System.out.println("[Agent Info]");
        System.out.println("  Name: " + getAID().getLocalName());
        System.out.println("  Full Name: " + getAID().getName());
        
        // Check arguments
        Object[] args = getArguments();
        if (args != null && args.length >= 2) {
            String mode = args[0].toString();
            if ("send".equalsIgnoreCase(mode)) {
                isSender = true;
                targetAgent = args[1].toString();
                System.out.println("  Mode: SENDER");
                System.out.println("  Target: " + targetAgent);
            }
        }
        
        if (!isSender) {
            System.out.println("  Mode: RECEIVER");
            // Add receiver behaviour
            addBehaviour(new MessageReceiverBehaviour());
            System.out.println("\n[Ready] Listening for incoming messages...\n");
        } else {
            // Send a test message
            sendTestMessage();
        }
    }
    
    /**
     * Send a test message to another agent
     */
    private void sendTestMessage() {
        System.out.println("\n[Sending Message]");
        
        // Create message
        ACLMessage msg = new ACLMessage(ACLMessage.INFORM);
        
        // Set receiver
        AID receiver = new AID(targetAgent, AID.ISLOCALNAME);
        msg.addReceiver(receiver);
        
        // Set content
        String content = "Hello from " + getAID().getLocalName() + "! Time: " + System.currentTimeMillis();
        msg.setContent(content);
        
        // Set conversation metadata
        msg.setConversationId("week2-lab");
        msg.setReplyWith("msg-" + System.currentTimeMillis());
        
        // Send
        send(msg);
        System.out.println("  Performative: INFORM");
        System.out.println("  To: " + targetAgent);
        System.out.println("  Content: " + content);
        System.out.println("  ConversationId: " + msg.getConversationId());
        System.out.println("\n[Message Sent Successfully!]\n");
        
        // Add a behaviour to wait for reply
        addBehaviour(new CyclicBehaviour() {
            private int waitCount = 0;
            
            @Override
            public void action() {
                MessageTemplate mt = MessageTemplate.MatchConversationId("week2-lab");
                ACLMessage reply = myAgent.receive(mt);
                
                if (reply != null) {
                    System.out.println("[Reply Received]");
                    System.out.println("  From: " + reply.getSender().getLocalName());
                    System.out.println("  Content: " + reply.getContent());
                    System.out.println("\n[Communication Complete!]");
                    myAgent.doDelete();
                } else {
                    waitCount++;
                    if (waitCount > 10) {
                        System.out.println("  (Waiting for reply... " + waitCount + ")");
                        waitCount = 0;
                    }
                    block(500); // Wait 500ms before checking again
                }
            }
        });
    }
    
    /**
     * Cyclic behaviour to receive and respond to messages
     */
    private class MessageReceiverBehaviour extends CyclicBehaviour {
        
        @Override
        public void action() {
            // Receive any message
            ACLMessage msg = receive();
            
            if (msg != null) {
                System.out.println("[Message Received]");
                System.out.println("  Performative: " + ACLMessage.getPerformative(msg.getPerformative()));
                System.out.println("  From: " + msg.getSender().getLocalName());
                System.out.println("  Content: " + msg.getContent());
                System.out.println("  ConversationId: " + msg.getConversationId());
                
                // Send reply
                ACLMessage reply = msg.createReply();
                reply.setPerformative(ACLMessage.CONFIRM);
                reply.setContent("Message received by " + myAgent.getAID().getLocalName() + "!");
                myAgent.send(reply);
                
                System.out.println("\n[Reply Sent]");
                System.out.println("  Performative: CONFIRM");
                System.out.println("  Content: " + reply.getContent());
                System.out.println("\n[Ready] Listening for more messages...\n");
            } else {
                // Block until a message arrives
                block();
            }
        }
    }
    
    @Override
    protected void takeDown() {
        System.out.println("\n[Agent Terminating]");
        System.out.println("  " + getAID().getLocalName() + " shutting down.\n");
    }
}
