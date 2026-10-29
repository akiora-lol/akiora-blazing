package A;

import jade.core.Agent;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.core.behaviours.TickerBehaviour;
import jade.lang.acl.ACLMessage;

import java.util.List;

public class AMain extends Agent {

    @Override
    protected void setup() {
        System.out.println("Привет! агент " + getAID().getName() + " готов.");
        addBehaviour(new CyclicBehaviour(this) {
            @Override
            public void action() {
                ACLMessage msg = receive();
                if (msg != null) {
                    System.out.printf("%s received %s from %s%n",
                            getLocalName(), msg.getContent(), msg.getSender().getLocalName());
                } else {
                    block();
                }
            }
        });

        // Repeat the exchange so it can be observed in the JADE Sniffer tool.
        addBehaviour(new TickerBehaviour(this, 5_000) {
            @Override
            protected void onTick() {
                sendPings();
            }
        });
    }

    private void sendPings() {
        for (String receiverName : List.of("agentb", "B")) {
            ACLMessage ping = new ACLMessage(ACLMessage.REQUEST);
            ping.addReceiver(new AID(receiverName, AID.ISLOCALNAME));
            ping.setLanguage("English");
            ping.setContent("Ping");
            send(ping);
            System.out.printf("%s sent Ping to %s%n", getLocalName(), receiverName);
        }
    }
}
