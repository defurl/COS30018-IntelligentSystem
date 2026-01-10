package week1;

import jade.core.Agent;

public class HelloAgent extends Agent {
    protected void setup() {
        System.out.println("Hello! Agent " + getAID().getName() + " is ready.");
        
        // Print arguments if any
        Object[] args = getArguments();
        if (args != null && args.length > 0) {
            System.out.println("Arguments received:");
            for (int i = 0; i < args.length; i++) {
                System.out.println("- " + args[i]);
            }
        }
    }
    
    protected void takeDown() {
        System.out.println("Agent " + getAID().getName() + " terminating.");
    }
}
