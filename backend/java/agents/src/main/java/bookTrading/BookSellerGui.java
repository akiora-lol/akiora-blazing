package bookTrading;

import java.awt.GridLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.*;

public class BookSellerGui extends JFrame {
    public BookSellerGui(BookSellerAgent seller) {
        super("Каталог продавца: " + seller.getLocalName());
        JTextField title = new JTextField(22);
        JTextField price = new JTextField(22);
        JButton add = new JButton("Добавить / обновить");
        JPanel panel = new JPanel(new GridLayout(3, 2, 8, 8));
        panel.setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));
        panel.add(new JLabel("Название (без пробелов):")); panel.add(title);
        panel.add(new JLabel("Цена (целое число > 0):")); panel.add(price);
        panel.add(new JLabel("Пример: Java_programming")); panel.add(add);
        add.setActionCommand("add");
        add.addActionListener(event -> {
            try {
                String name = title.getText().trim();
                int value = Integer.parseInt(price.getText().trim());
                if (name.isEmpty() || name.chars().anyMatch(Character::isWhitespace) || value <= 0)
                    throw new IllegalArgumentException();
                seller.updateCatalogue(name, value);
                title.setText(""); price.setText(""); title.requestFocusInWindow();
            } catch (IllegalArgumentException ex) {
                JOptionPane.showMessageDialog(this, "Введите название без пробелов и положительную целую цену.");
            }
        });
        setContentPane(panel);
        setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent event) { seller.doDelete(); }
        });
        pack(); setLocationByPlatform(true);
    }
}
