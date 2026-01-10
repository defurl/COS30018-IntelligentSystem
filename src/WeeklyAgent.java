import jade.core.Agent;

public class WeeklyAgent extends Agent {
    protected void setup() {
        System.out.println("WeeklyAgent " + getAID().getName() + " is online!");
    }
}
