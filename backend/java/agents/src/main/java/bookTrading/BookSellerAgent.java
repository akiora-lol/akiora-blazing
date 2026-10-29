package bookTrading;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.core.behaviours.OneShotBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import java.awt.GraphicsEnvironment;
import java.util.HashMap;
import java.util.Map;
import javax.swing.SwingUtilities;

public class BookSellerAgent extends Agent {
    private final Map<String, Integer> catalogue = new HashMap<>();
    private BookSellerGui gui;
    private boolean registered;

    protected void setup() {
        // Необязательные аргументы: Java_programming=500, Clean_code=700.
        Object[] args = getArguments();
        if (args != null) for (Object arg : args) {
            String[] entry = arg.toString().split("=", 2);
            try {
                int price = Integer.parseInt(entry[1]);
                if (entry[0].isBlank() || price <= 0) throw new IllegalArgumentException();
                catalogue.put(entry[0], price);
            } catch (RuntimeException ex) {
                System.out.println(getLocalName() + ": invalid catalogue entry " + arg);
            }
        }
        DFAgentDescription description = new DFAgentDescription();
        description.setName(getAID());
        ServiceDescription service = new ServiceDescription();
        service.setType("book-selling");
        service.setName("JADE-book-trading");
        description.addServices(service);
        try {
            DFService.register(this, description);
            registered = true;
        } catch (FIPAException ex) {
            ex.printStackTrace();
            doDelete();
            return;
        }
        System.out.println(getLocalName() + " ready: " + catalogue);
        if (!GraphicsEnvironment.isHeadless()) SwingUtilities.invokeLater(() -> {
            gui = new BookSellerGui(this);
            gui.setVisible(true);
        });
        // Два независимых циклических поведения разделяют сообщения по типу.
        addBehaviour(new CyclicBehaviour() {
            public void action() {
                ACLMessage request = receive(MessageTemplate.and(
                    MessageTemplate.MatchConversationId("book-trade"),
                    MessageTemplate.MatchPerformative(ACLMessage.CFP)));
                if (request == null) { block(); return; }
                Integer price = catalogue.get(request.getContent());
                ACLMessage reply = request.createReply();
                reply.setPerformative(price == null ? ACLMessage.REFUSE : ACLMessage.PROPOSE);
                reply.setContent(price == null ? "not-available" : price.toString());
                send(reply);
                System.out.println(getLocalName() + " -> " + request.getSender().getLocalName()
                    + " " + ACLMessage.getPerformative(reply.getPerformative()) + " " + reply.getContent());
            }
        });
        addBehaviour(new CyclicBehaviour() {
            public void action() {
                ACLMessage order = receive(MessageTemplate.and(
                    MessageTemplate.MatchConversationId("book-trade"),
                    MessageTemplate.MatchPerformative(ACLMessage.ACCEPT_PROPOSAL)));
                if (order == null) { block(); return; }
                Integer price = catalogue.remove(order.getContent());
                ACLMessage reply = order.createReply();
                reply.setPerformative(price == null ? ACLMessage.FAILURE : ACLMessage.INFORM);
                reply.setContent(price == null ? "already-sold" : order.getContent());
                send(reply);
                System.out.println(getLocalName() + (price == null ? " cannot sell " : " sold ")
                    + order.getContent() + " to " + order.getSender().getLocalName());
            }
        });
    }

    public void updateCatalogue(String title, int price) {
        // Swing работает в другом потоке: изменение каталога передаётся потоку агента.
        addBehaviour(new OneShotBehaviour() {
            public void action() {
                catalogue.put(title, price);
                System.out.println(getLocalName() + " added " + title + " price=" + price);
            }
        });
    }

    protected void takeDown() {
        if (registered) try { DFService.deregister(this); }
        catch (FIPAException ex) { ex.printStackTrace(); }
        SwingUtilities.invokeLater(() -> { if (gui != null) gui.dispose(); });
        System.out.println(getLocalName() + " terminating.");
    }
}
