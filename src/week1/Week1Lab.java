package week1;

import jade.core.Agent;
import jade.core.AID;

/**
 * Week 1 Lab: Custom JADE Agent
 * 
 * This agent demonstrates:
 * 1. Basic agent setup and lifecycle
 * 2. Agent Identifier (AID) properties
 * 3. Receiving and processing arguments
 * 4. Agent termination
 * 
 * To run:
 *   java -cp lib/jade.jar jade.Boot -gui -platform-id MyPlatform -agents myAgent:week1.Week1Lab
 */
public class Week1Lab extends Agent {
    
    @Override
    protected void setup() {
        // Get Agent Identifier
        AID myAID = getAID();
        
        System.out.println("===========================================");
        System.out.println("       WEEK 1 LAB: JADE Agent Basics       ");
        System.out.println("===========================================");
        
        // 1. Print basic agent information
        System.out.println("\n[Agent Information]");
        System.out.println("  Local Name: " + myAID.getLocalName());
        System.out.println("  GUID (Global Name): " + myAID.getName());
        
        // 2. Print agent addresses
        String[] addresses = myAID.getAddressesArray();
        System.out.println("\n[Agent Addresses]");
        if (addresses.length > 0) {
            for (String addr : addresses) {
                System.out.println("  - " + addr);
            }
        } else {
            System.out.println("  (No addresses registered yet)");
        }
        
        // 3. Print container and platform info
        System.out.println("\n[Platform Information]");
        try {
            System.out.println("  Container: " + getContainerController().getContainerName());
        } catch (Exception e) {
            System.out.println("  Container: (unable to retrieve)");
        }
        
        // 4. Process command-line arguments
        Object[] args = getArguments();
        System.out.println("\n[Command-line Arguments]");
        if (args != null && args.length > 0) {
            for (int i = 0; i < args.length; i++) {
                System.out.println("  Arg[" + i + "]: " + args[i]);
            }
        } else {
            System.out.println("  (No arguments provided)");
        }
        
        // 5. Agent states demonstration
        System.out.println("\n[Agent State]");
        System.out.println("  Current State: ACTIVE");
        System.out.println("  Agent is now running and ready for behaviours!");
        
        System.out.println("\n===========================================");
        System.out.println("  Agent setup complete! Use RMA GUI to");
        System.out.println("  interact with this agent.");
        System.out.println("===========================================\n");
    }
    
    @Override
    protected void takeDown() {
        // Cleanup when agent is terminated
        System.out.println("\n[Agent Termination]");
        System.out.println("  Agent " + getAID().getLocalName() + " is shutting down.");
        System.out.println("  Cleanup complete. Goodbye!");
    }
}
