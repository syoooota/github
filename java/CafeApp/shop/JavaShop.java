package shop;

import java.applet.Applet;
import java.awt.BorderLayout;
import java.awt.Button;
import java.awt.CardLayout;
import java.awt.Checkbox;
import java.awt.CheckboxGroup;
import java.awt.Choice;
import java.awt.Color;
import java.awt.Component;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Label;
import java.awt.List;
import java.awt.Panel;
import java.awt.TextArea;
import java.awt.TextField;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.HashMap;
import java.util.Map;

@SuppressWarnings("serial")
public class JavaShop extends Applet implements ActionListener, ItemListener {
//	 business model
	String name, page, drink;
	Order cart;
	int y, z;
	InventoryDB inventory;
	String take, s;
	TextField t1;
	Choice c1, c2;
	// view
	Panel parent;
	Label label;
	CardLayout pages;
	Map<String, Component> gui; // 螟壹￥縺ｮ驛ｨ蜩√ｒ蟆代↑縺・ｽ螟画焚縺ｧ謇ｱ縺・ｽ

	public void init() {
		name = "Java Cafe";
		cart = new Order();
		inventory = InventoryDB.createInventoryDB();

		setSize(320, 320);
		initGUI();

	}

	public void initGUI() {
		gui = new HashMap<String, Component>();

		// 逕ｻ髱｢荳企Κ縺ｫ繧ｿ繧､繝医Ν繧貞崋螳・ｽ
		setLayout(new BorderLayout());
		label = new Label("Welcome to " + name, Label.CENTER);

		add(label);
		add(label, BorderLayout.NORTH);

		// 繧ｿ繧､繝医Ν莉･螟悶ｒ蛻・ｽ繧頑崛縺郁｡ｨ遉ｺ
		parent = new Panel();
		{
			pages = new CardLayout();
			parent.setLayout(pages);

			parent.add(createAccountPanel(), "account");
			parent.add(createOrderPanel(), "order");
			parent.add(createEatPanel(), "eat");
			parent.add(createBringPanel(), "bring");
			parent.add(createSsizedrinkPanel(), "ssizedrink");
			parent.add(createMsizedrinkPanel(), "msizedrink");
			parent.add(createLsizedrinkPanel(), "lsizedrink");
			parent.add(createCheckPanel(), "check");
			parent.add(createSizecheckPanel(), "sizecheck");
			parent.add(createEatcheckPanel(), "eatcheck");
			parent.add(createPayPanel(), "pay");
			parent.add(createReceiptPanel(), "receipt");
			parent.add(createSurveyPanel(), "survey");
			parent.add(createErrorPanel(), "error");

		}
		add(parent, BorderLayout.CENTER);

		showPage("account");
	}

	Panel createAccountPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());
			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("      ");
				l1.setForeground(Color.red);
				gbc.anchor = GridBagConstraints.NORTH;
				gbc.gridx = 0;
				gbc.gridy = 5;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				gui.put("account.label", l1);
				p.add(l1);

				Label ID = new Label("Name");
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(ID, gbc);
				p.add(ID);

				Label pass = new Label("Pass");
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(pass, gbc);
				p.add(pass);

				TextField t1 = new TextField(15);
				t1.addActionListener(this);
				gui.put("account.name", t1);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(t1, gbc);
				p.add(t1);

				TextField t2 = new TextField(15);
				t2.addActionListener(this);
				gui.put("account.pass", t2);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(t2, gbc);
				p.add(t2);

			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{

				Button guest = new Button("Guest");
				guest.addActionListener(this);
				pb.add(guest);

				Button ok = new Button("Login");
				ok.addActionListener(this);
				pb.add(ok);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createSsizedrinkPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Item:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				List itemList = new List(10);

				Item item1 = ItemDB.search(0);
				itemList.add(item1.getName() + " @(bring)" + item1.getPrice()
						/ 10 * 7);
				Item item2 = ItemDB.search(2);
				itemList.add(item2.getName() + " @(bring)" + item2.getPrice()
						/ 10 * 7);
				Item item3 = ItemDB.search(5);
				itemList.add(item3.getName() + " @(bring)" + item3.getPrice()
						/ 10 * 7);

				itemList.setSize(140, 200);
				itemList.addItemListener(this);
				gui.put("s.item", itemList);
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(itemList, gbc);
				p.add(itemList);

				Label l2 = new Label("Count:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l2, gbc);
				p.add(l2);

				TextField countText = new TextField(5);
				countText.addActionListener(this);
				gui.put("s.count", countText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(countText, gbc);
				p.add(countText);

				Label l3 = new Label("Total:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField totalText = new TextField(10);
				totalText.setEditable(false);
				gui.put("s.total", totalText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(totalText, gbc);
				p.add(totalText);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{

				Button add = new Button("Pour");
				add.addActionListener(this);
				pb.add(add);

				Button check = new Button("Cart");
				check.addActionListener(this);
				pb.add(check);

				Button con = new Button("Continue");
				con.addActionListener(this);
				pb.add(con);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createMsizedrinkPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Item:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				List itemList = new List(10);
				Item item1 = ItemDB.search(1);
				itemList.add(item1.getName() + " @(bring)" + item1.getPrice()
						/ 10 * 7);
				Item item2 = ItemDB.search(3);
				itemList.add(item2.getName() + " @(bring)" + item2.getPrice()
						/ 10 * 7);
				Item item3 = ItemDB.search(6);
				itemList.add(item3.getName() + " @(bring)" + item3.getPrice()
						/ 10 * 7);
				itemList.setSize(140, 200);
				itemList.addItemListener(this);
				gui.put("m.item", itemList);
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(itemList, gbc);
				p.add(itemList);

				Label l2 = new Label("Count:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l2, gbc);
				p.add(l2);

				TextField countText = new TextField(5);
				countText.addActionListener(this);
				gui.put("m.count", countText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(countText, gbc);
				p.add(countText);

				Label l3 = new Label("Total:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField totalText = new TextField(10);
				totalText.setEditable(false);
				gui.put("m.total", totalText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(totalText, gbc);
				p.add(totalText);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{

				Button add = new Button("Pour");
				add.addActionListener(this);
				pb.add(add);

				Button check = new Button("Cart");
				check.addActionListener(this);
				pb.add(check);

				Button con = new Button("Continue");
				con.addActionListener(this);
				pb.add(con);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createLsizedrinkPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Item:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				List itemList = new List(10);
				Item item1 = ItemDB.search(4);
				itemList.add(item1.getName() + " @(bring)" + item1.getPrice()
						/ 10 * 7);
				Item item2 = ItemDB.search(7);
				itemList.add(item2.getName() + " @(bring)" + item2.getPrice()
						/ 10 * 7);
				Item item3 = ItemDB.search(8);
				itemList.add(item3.getName() + " @(bring)" + item3.getPrice()
						/ 10 * 7);
				itemList.setSize(140, 200);
				itemList.addItemListener(this);
				gui.put("l.item", itemList);
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(itemList, gbc);
				p.add(itemList);

				Label l2 = new Label("Count:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l2, gbc);
				p.add(l2);

				TextField countText = new TextField(5);
				countText.addActionListener(this);
				gui.put("l.count", countText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(countText, gbc);
				p.add(countText);

				Label l3 = new Label("Total:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField totalText = new TextField(10);
				totalText.setEditable(false);
				gui.put("l.total", totalText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(totalText, gbc);
				p.add(totalText);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{

				Button add = new Button("Pour");
				add.addActionListener(this);
				pb.add(add);

				Button check = new Button("Cart");
				check.addActionListener(this);
				pb.add(check);

				Button con = new Button("Continue");
				con.addActionListener(this);
				pb.add(con);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createOrderPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Drink item:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				List itemList = new List(10);
				int n = ItemDB.getItems();
				for (int i = 0; i < n; i++) {
					Item item = ItemDB.search(i);
					itemList.add(item.getName() + " @" + item.getPrice());
				}
				itemList.setSize(140, 200);
				itemList.addItemListener(this);
				gui.put("order.item", itemList);
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(itemList, gbc);
				p.add(itemList);

				Panel rl = new Panel();
				{
					Button l = new Button("<");
					l.addActionListener(this);
					rl.add(l);
					Button r = new Button(">");
					r.addActionListener(this);
					rl.add(r);
				}
				gbc.anchor = GridBagConstraints.CENTER;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(rl, gbc);
				p.add(rl);

				Label l2 = new Label("Count:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l2, gbc);
				p.add(l2);

				TextField countText = new TextField(5);
				countText.addActionListener(this);
				gui.put("order.count", countText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(countText, gbc);
				p.add(countText);

				Label l3 = new Label("Total:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField totalText = new TextField(10);
				totalText.setEditable(false);
				gui.put("order.total", totalText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(totalText, gbc);
				p.add(totalText);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{
				Button add = new Button("Add");
				add.addActionListener(this);
				pb.add(add);

				Button check = new Button("Cart");
				check.addActionListener(this);
				pb.add(check);

				Button cup = new Button("Bring your own cup");
				cup.addActionListener(this);
				pb.add(cup);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createEatPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Food item:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				List itemList = new List(10);
				int n = EatDB.getItems();
				for (int i = 0; i < n; i++) {
					Eat item = EatDB.search(i);
					itemList.add(item.getName() + " @" + item.getPrice());
				}
				itemList.setSize(200, 230);
				itemList.addItemListener(this);
				gui.put("eat.item", itemList);
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(itemList, gbc);
				p.add(itemList);

				Panel rl = new Panel();
				{
					Button l = new Button("<");
					l.addActionListener(this);
					rl.add(l);
					Button r = new Button(">");
					r.addActionListener(this);
					rl.add(r);
				}
				gbc.anchor = GridBagConstraints.CENTER;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(rl, gbc);
				p.add(rl);

				Label l2 = new Label("Count:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l2, gbc);
				p.add(l2);

				TextField countText = new TextField(5);
				countText.addActionListener(this);
				gui.put("eat.count", countText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(countText, gbc);
				p.add(countText);

				Label l3 = new Label("Total:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField eattotalText = new TextField(10);
				eattotalText.setEditable(false);
				gui.put("eat.total", eattotalText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(eattotalText, gbc);
				p.add(eattotalText);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{
				Button add = new Button("Add");
				add.addActionListener(this);
				pb.add(add);

				Button check = new Button("Cart");
				check.addActionListener(this);
				pb.add(check);

				Button cup = new Button("Bring your own cup");
				cup.addActionListener(this);
				pb.add(cup);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createBringPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Size", Label.LEFT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				c1 = new Choice();
				c1.add("");
				c1.add("S");
				c1.add("M");
				c1.add("L");
				c1.addItemListener(this);
				gbc.gridx = 0;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(c1, gbc);
				p.add(c1);

				Label l2 = new Label("Type", Label.LEFT);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l2, gbc);
				p.add(l2);

				c2 = new Choice();
				c2.add("");
				c2.add("Plastic");
				c2.add("Glass");
				c2.addItemListener(this);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(c2, gbc);
				p.add(c2);

				Label l3 = new Label("Quantity", Label.LEFT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 2;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField t1 = new TextField(2);
				t1.addActionListener(this);
				gui.put("bring.count", t1);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 2;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(t1, gbc);
				p.add(t1);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{
				Button add = new Button("Next");
				add.addActionListener(this);
				pb.add(add);

				Button back = new Button("Back");
				back.addActionListener(this);
				pb.add(back);
			}
			page.add(pb, BorderLayout.SOUTH);
		}

		return page;
	}

	Panel createCheckPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Order drinks:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				List orderList = new List(10, true);
				orderList.setSize(140, 200);
				orderList.addItemListener(this);
				gui.put("check.order", orderList);
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(orderList, gbc);
				p.add(orderList);

				Panel rl = new Panel();
				{
					Button l = new Button("<");
					l.addActionListener(this);
					rl.add(l);
					Button r = new Button(">");
					r.addActionListener(this);
					rl.add(r);
				}
				gbc.anchor = GridBagConstraints.CENTER;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(rl, gbc);
				p.add(rl);

				Label l3 = new Label("Total:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField totalText = new TextField(10);
				totalText.setEditable(false);
				gui.put("check.total", totalText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(totalText, gbc);
				p.add(totalText);

				Panel buttons = new Panel();
				{
					Button inc = new Button("+1");
					inc.addActionListener(this);
					buttons.add(inc);
					Button dec = new Button("-1");
					dec.addActionListener(this);
					buttons.add(dec);
				}
				gbc.gridx = 1;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(buttons, gbc);
				p.add(buttons);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{
				Button check = new Button("Continue");
				check.addActionListener(this);
				pb.add(check);

				Button add = new Button("Check");
				add.addActionListener(this);
				pb.add(add);

				Button takeout = new Button("Take out");

				takeout.addActionListener(this);
				pb.add(takeout);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createSizecheckPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Pour drink:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				List offorderList = new List(10, true);
				offorderList.setSize(140, 200);
				offorderList.addItemListener(this);
				gui.put("check.offorder", offorderList);
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(offorderList, gbc);
				p.add(offorderList);

				Panel rl = new Panel();
				{
					Button l = new Button("<");
					l.addActionListener(this);
					rl.add(l);
					Button r = new Button(">");
					r.addActionListener(this);
					rl.add(r);
				}
				gbc.anchor = GridBagConstraints.CENTER;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(rl, gbc);
				p.add(rl);

				Label l3 = new Label("30%off Total:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField totalText = new TextField(10);
				totalText.setEditable(false);
				gui.put("check.offtotal", totalText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(totalText, gbc);
				p.add(totalText);

				Panel buttons = new Panel();
				{
					Button inc = new Button("+1");
					inc.addActionListener(this);
					buttons.add(inc);
					Button dec = new Button("-1");
					dec.addActionListener(this);
					buttons.add(dec);
				}
				gbc.gridx = 1;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(buttons, gbc);
				p.add(buttons);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{
				Button check = new Button("Continue");
				check.addActionListener(this);
				pb.add(check);

				Button add = new Button("Check");
				add.addActionListener(this);
				pb.add(add);

				Button takeout = new Button("Take out");

				takeout.addActionListener(this);
				pb.add(takeout);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createEatcheckPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Order foods:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				List orderList = new List(10, true);
				orderList.setSize(140, 200);
				orderList.addItemListener(this);
				gui.put("eatcheck.order", orderList);
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(orderList, gbc);
				p.add(orderList);

				Panel rl = new Panel();
				{
					Button l = new Button("<");
					l.addActionListener(this);
					rl.add(l);
					Button r = new Button(">");
					r.addActionListener(this);
					rl.add(r);
				}
				gbc.anchor = GridBagConstraints.CENTER;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(rl, gbc);
				p.add(rl);

				Label l3 = new Label("Total:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField totalText = new TextField(10);
				totalText.setEditable(false);
				gui.put("eatcheck.total", totalText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(totalText, gbc);
				p.add(totalText);

				Panel buttons = new Panel();
				{
					Button inc = new Button("+1");
					inc.addActionListener(this);
					buttons.add(inc);
					Button dec = new Button("-1");
					dec.addActionListener(this);
					buttons.add(dec);
				}
				gbc.gridx = 1;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(buttons, gbc);
				p.add(buttons);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{
				Button check = new Button("Continue");
				check.addActionListener(this);
				pb.add(check);

				Button add = new Button("Check");
				add.addActionListener(this);
				pb.add(add);

				Button takeout = new Button("Take out");

				takeout.addActionListener(this);
				pb.add(takeout);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createPayPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				GridBagLayout layout = new GridBagLayout();
				GridBagConstraints gbc = new GridBagConstraints();
				p.setLayout(layout);

				Label l1 = new Label("Order:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l1, gbc);
				p.add(l1);

				List orderList = new List(10, true);
				orderList.setSize(140, 200);
				orderList.addItemListener(this);
				gui.put("pay.order", orderList);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 0;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(orderList, gbc);
				p.add(orderList);

				Label l3 = new Label("Total:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l3, gbc);
				p.add(l3);

				TextField totalText = new TextField(10);
				totalText.setEditable(false);
				gui.put("pay.total", totalText);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 1;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(totalText, gbc);
				p.add(totalText);

				Label l4 = new Label("Credit Card:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l4, gbc);
				p.add(l4);

				TextField credit = new TextField(16);
				gui.put("pay.credit", credit);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 2;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(credit, gbc);
				p.add(credit);

				Label l5 = new Label("Card Holder:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l5, gbc);
				p.add(l5);

				TextField holder = new TextField(16);
				gui.put("pay.holder", holder);
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 3;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(holder, gbc);
				p.add(holder);

				Label l6 = new Label("Expiration Date:", Label.RIGHT);
				gbc.anchor = GridBagConstraints.NORTHEAST;
				gbc.gridx = 0;
				gbc.gridy = 4;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(l6, gbc);
				p.add(l6);

				Panel date = new Panel();
				{
					TextField mm = new TextField("mm", 2);
					gui.put("pay.month", mm);
					date.add(mm);
					TextField yy = new TextField("yy", 2);
					gui.put("pay.year", yy);
					date.add(yy);
				}
				gbc.anchor = GridBagConstraints.NORTHWEST;
				gbc.gridx = 1;
				gbc.gridy = 4;
				gbc.gridwidth = 1;
				gbc.gridheight = 1;
				layout.setConstraints(date, gbc);
				p.add(date);
			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{
				Button cancel = new Button("Cancel");
				cancel.addActionListener(this);
				pb.add(cancel);

				Button pay = new Button("Pay");
				pay.addActionListener(this);
				pb.add(pay);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createReceiptPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			TextArea receiptText = new TextArea(10, 10);
			gui.put("receipt.receipt", receiptText);
			page.add(receiptText, BorderLayout.CENTER);

			Panel pb = new Panel();
			{
				Button ok = new Button("Continue");
				ok.addActionListener(this);
				pb.add(ok);

				Button sur = new Button("Survey");
				sur.addActionListener(this);
				pb.add(sur);

				Button end = new Button("End");
				end.addActionListener(this);
				pb.add(end);
			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	Panel createErrorPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());

			Panel p = new Panel();
			{
				p.add(new Label("Sold out. Your order will be canceled."));

				Panel pb = new Panel();
				{
					Button pay = new Button("OK");
					pay.addActionListener(this);
					pb.add(pay);
				}
				page.add(pb, BorderLayout.SOUTH);
			}
			page.add(p);
		}
		return page;
	}

	Panel createSurveyPanel() {
		Panel page = new Panel();
		{
			page.setLayout(new BorderLayout());
			Panel p = new Panel();
			{

				Label l1 = new Label("Drink nemu :");
				p.add(l1);
				CheckboxGroup cg = new CheckboxGroup();
				Checkbox c1 = new Checkbox("Expresso", false, cg);
				gui.put("exp", c1);
				p.add(c1);
				c1.addItemListener(this);
				Checkbox c2 = new Checkbox("Arabica", false, cg);
				p.add(c2);
				gui.put("ara", c2);
				c2.addItemListener(this);
				Checkbox c3 = new Checkbox("Robusta", false, cg);
				p.add(c3);
				gui.put("rob", c3);
				c3.addItemListener(this);
				Checkbox c4 = new Checkbox("Java", false, cg);
				p.add(c4);
				gui.put("java", c4);
				c4.addItemListener(this);

			}
			page.add(p, BorderLayout.CENTER);

			Panel pb = new Panel();
			{

				Button guest = new Button("End");
				guest.addActionListener(this);
				pb.add(guest);

			}
			page.add(pb, BorderLayout.SOUTH);
		}
		return page;
	}

	void showPage(String name) {
		pages.show(parent, name);
		page = name;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		if (e.getSource() == gui.get("order.count")) {
			Item item = getSelectedItem();
			if (item != null) {
				int price = item.getPrice();
				TextField countText = (TextField) gui.get("order.count");
				int count = Integer.parseInt(countText.getText());
				TextField totalText = (TextField) gui.get("order.total");
				totalText.setText("" + (price * count));

			}
		}

		if (e.getSource() == gui.get("eat.count")) {
			Eat item = getSelectedEat();
			if (item != null) {
				int price = item.getPrice();
				TextField countText = (TextField) gui.get("eat.count");
				int count = Integer.parseInt(countText.getText());
				TextField totalText = (TextField) gui.get("eat.total");
				totalText.setText("" + (price * count));

			}
		}

		if (e.getSource() == gui.get("s.count")) {
			Item item = getSItem();
			if (item != null) {
				int price = item.getPrice() / 10 * 7;
				TextField countText = (TextField) gui.get("s.count");
				int count = Integer.parseInt(countText.getText());

				TextField totalText = (TextField) gui.get("s.total");
				totalText.setText("" + (price * count));

			}
		}

		if (e.getSource() == gui.get("m.count")) {
			Item item = getMItem();
			if (item != null) {
				int price = item.getPrice();
				TextField countText = (TextField) gui.get("m.count");
				int count = Integer.parseInt(countText.getText());
				TextField totalText = (TextField) gui.get("m.total");
				totalText.setText("" + (price * count));

			}
		}

		if (e.getSource() == gui.get("l.count")) {
			Item item = getLItem();
			if (item != null) {
				int price = item.getPrice();
				TextField countText = (TextField) gui.get("l.count");
				int count = Integer.parseInt(countText.getText());
				TextField totalText = (TextField) gui.get("l.total");
				totalText.setText("" + (price * count));

			}
		}

		if (e.getActionCommand().equals("Login")) {
			try {
				TextField t1 = (TextField) gui.get("account.name");
				Credit a = CreditDB.search3(t1.getText());
				TextField t2 = (TextField) gui.get("account.pass");
				Credit b = CreditDB.search2(t2.getText());
				Label l1 = (Label) gui.get("account.label");
				if (a.getHolder().equals(b.getHolder())) {
					showPage("order");
					TextField creditText = (TextField) gui.get("pay.credit");
					TextField holderText = (TextField) gui.get("pay.holder");
					TextField mm = (TextField) gui.get("pay.month");
					TextField yy = (TextField) gui.get("pay.year");
					creditText.setText(a.getNumber());
					holderText.setText(a.getHolder());
					mm.setText(a.getDatem());
					yy.setText(a.getDatey());
				} else {
					l1.setText("error");
				}
			} catch (NullPointerException e1) {
				Label l1 = (Label) gui.get("account.label");
				l1.setText("error");
			}
		}

		if (e.getActionCommand().equals("Guest")) {
			showPage("order");

		}

		if (e.getActionCommand().equals("Add")) {

			if (page.equals("order")) {
				Item item = getSelectedItem();
				if (item != null) {
					TextField countText = (TextField) gui.get("order.count");
					int count = Integer.parseInt(countText.getText());
					cart.add(item, count);
					updateCheck();
				}
			} else if (page.equals("eat")) {
				Eat item2 = getSelectedEat();
				if (item2 != null) {
					TextField countText = (TextField) gui.get("eat.count");
					int count = Integer.parseInt(countText.getText());
					cart.add3(item2, count);
					updateCheck3();
				}
			}

		}
		if (e.getActionCommand().equals("Pour")) {

			if (y != 0) {
				y--;

				if (s.equals("S")) {
					Item item = getSItem();
					if (item != null) {
						TextField countText = (TextField) gui.get("s.count");
						int count = Integer.parseInt(countText.getText());
						cart.add2(item, count);
					}
				}
				if (s.equals("M")) {
					Item item = getMItem();
					if (item != null) {
						TextField countText = (TextField) gui.get("m.count");
						int count = Integer.parseInt(countText.getText());
						cart.add2(item, count);
					}
				}
				if (s.equals("L")) {
					Item item = getLItem();
					if (item != null) {
						TextField countText = (TextField) gui.get("l.count");
						int count = Integer.parseInt(countText.getText());
						cart.add2(item, count);
					}
				}
			}
			updateCheck2();
		}
		if (e.getActionCommand().equals("Bring your own cup")) {
			showPage("bring");

		}
		if (e.getActionCommand().equals("Back")) {
			pages.previous(parent);

		}

		if (e.getActionCommand().equals("Cart")) {
			showPage("check");

		}

		if (e.getActionCommand().equals("<")) {
			if (page.equals("eat")) {
				showPage("order");
			} else if (page.equals("sizecheck")) {
				showPage("check");
			} else if (page.equals("eatcheck")) {
				showPage("sizecheck");

			}

		}

		if (e.getActionCommand().equals(">")) {
			if (page.equals("order")) {
				showPage("eat");
			} else if (page.equals("sizecheck")) {
				showPage("eatcheck");
			} else if (page.equals("check")) {
				showPage("sizecheck");

			}

		}

		if (e.getActionCommand().equals("+1")) {
			if (page.equals("check")) {
				for (Item item : getSelectedItems()) {
					cart.add(item, 1);
				}
				updateCheck();
			} else if (y != 0 && page.equals("sizecheck")) {
				for (Item item : getSelectedoffItems()) {
					cart.add2(item, 1);
				}
				y--;
				updateCheck2();
			} else if (page.equals("eatcheck")) {
				for (Eat item : getSelectedeatItems()) {
					cart.add3(item, 1);
				}
				updateCheck3();
			}

		}
		if (e.getActionCommand().equals("-1")) {
			if (page.equals("check")) {
				for (Item item : getSelectedItems()) {
					cart.add(item, -1);
				}
				updateCheck();
			} else if (page.equals("sizecheck")) {
				for (Item item : getSelectedoffItems()) {
					cart.add2(item, -1);
				}
				if (y < z) {
					y++;
				}
				updateCheck2();
			} else if (page.equals("eatcheck")) {
				for (Eat item : getSelectedeatItems()) {
					cart.add3(item, -1);
				}
				updateCheck3();
			}
		}

		if (e.getActionCommand().equals("Continue")) {

			label.setText("Welcome to " + name);
			take = "";
			showPage("order");
		}

		if (e.getActionCommand().equals("Take out")) {
			label.setText("See you");
			take = "Take out";
			if (inventory.canShip(cart)) {
				// 蝨ｨ蠎ｫ縺後≠繧後・ｽｰ謾ｯ謇輔＞縺ｸ
				if (cart.getItems().size() > 0) {
					updatePay();
					showPage("pay");
				}
			} else {
				// 縺昴≧縺ｧ縺ｪ縺代ｌ縺ｰ繧ｨ繝ｩ繝ｼ縺ｸ
				showPage("error");
			}
		}

		if (e.getActionCommand().equals("Check")) {
			if (inventory.canShip(cart)) {
				// 蝨ｨ蠎ｫ縺後≠繧後・ｽｰ謾ｯ謇輔＞縺ｸ
				if (cart.getItems().size() > 0) {
					updatePay();
					showPage("pay");
				}

			} else if (inventory.canShip2(cart)) {
				// 蝨ｨ蠎ｫ縺後≠繧後・ｽｰ謾ｯ謇輔＞縺ｸ
				if (cart.geteatItems().size() > 0) {
					updatePay();
					showPage("pay");
				}
			} else if (inventory.canShip3(cart)) {
				// 蝨ｨ蠎ｫ縺後≠繧後・ｽｰ謾ｯ謇輔＞縺ｸ
				if (cart.getoffItems().size() > 0) {
					updatePay();
					showPage("pay");
				}
			} else {
				// 縺昴≧縺ｧ縺ｪ縺代ｌ縺ｰ繧ｨ繝ｩ繝ｼ縺ｸ
				showPage("error");
			}

		}
		if (e.getActionCommand().equals("Cancel")) {
			label.setText("Welcome to " + name);
			take = "";
			showPage("check");
		}
		if (e.getActionCommand().equals("Pay")) {
			TextField creditText = (TextField) gui.get("pay.credit");
			String credit = creditText.getText();
			if (credit.length() != 16) {
				creditText.setText("not 16 digits");
				return;
			}
			TextField holderText = (TextField) gui.get("pay.holder");
			String holder = holderText.getText();
			if (holder.length() == 0) {
				holderText.setText("empty");
				return;
			}
			TextField mmText = (TextField) gui.get("pay.month");
			String mm = mmText.getText();
			try {
				int m = Integer.parseInt(mm);
				if (m < 1 || 12 < m) {
					mmText.setText("not 01-12");
					return;
				}
			} catch (NumberFormatException e1) {
				mmText.setText("not 01-12");
				return;
			}
			TextField yyText = (TextField) gui.get("pay.year");
			String yy = yyText.getText();
			try {
				int y = Integer.parseInt(mm);
				if (yy.length() != 2 || y < 0 || 100 <= y) {
					yyText.setText("not 00-99");
					return;
				}
			} catch (NumberFormatException e2) {
				yyText.setText("not 00-99");
				return;
			}
			if (inventory.canShip(cart)
					&& CreditDB.canPay(credit, holder, mm + "/" + yy)) {
				updateReceipt();
				showPage("receipt");
			} else {
				showPage("error");
			}
		}
		if (e.getActionCommand().equals("OK")) {
			label.setText("Welcome to " + name);
			take = "";
			showPage("order");
		}
		if (e.getActionCommand().equals("End")) {
			if (drink != null) {
				System.out.println("Best drink is " + drink);
			}
			System.exit(0);
		}
		if (e.getActionCommand().equals("Survey")) {
			label.setText("What the best drink?");
			showPage("survey");
		}
		if (e.getActionCommand().equals("Next")) {
			TextField t1 = (TextField) gui.get("bring.count");
			try {
				y = Integer.parseInt(t1.getText());
				z = Integer.parseInt(t1.getText());
				if (y < 0 || 10 < y) {
					t1.setText("not 00-10");
					return;
				}
			} catch (NumberFormatException e3) {
				t1.setText("not 00-10");
				return;
			}
			try {

				if (s.equals("S")) {
					showPage("ssizedrink");
				}
				if (s.equals("M")) {
					showPage("msizedrink");
				}
				if (s.equals("L")) {
					showPage("lsizedrink");
				}

			} catch (NullPointerException e2) {
				showPage("bring");
			}
		}
	}

	// update check page
	void updateCheck() {
		List orderList = (List) gui.get("check.order");
		int count = 0;
		int total = 0;
		orderList.removeAll();
		for (Item item : cart.getItems()) {
			int price = item.getPrice();
			count = cart.getItemCount(item);
			orderList.add(item.getName() + " x " + count);
			total += price * count;
		}
		TextField totalText = (TextField) gui.get("check.total");
		totalText.setText("" + total);
	}

	void updateCheck2() {
		List orderList = (List) gui.get("check.offorder");
		int count = 0;
		int total = 0;
		orderList.removeAll();
		for (Item item : cart.getoffItems()) {
			int price = item.getPrice() / 10 * 7;
			count = cart.getoffItemCount(item);
			orderList.add(item.getName() + " (bring)x " + count);
			total += price * count;
		}
		TextField totalText = (TextField) gui.get("check.offtotal");
		totalText.setText("" + total);
	}

	void updateCheck3() {
		List orderList = (List) gui.get("eatcheck.order");
		int count = 0;
		int total = 0;
		orderList.removeAll();
		for (Eat item : cart.geteatItems()) {
			int price = item.getPrice();
			count = cart.geteatItemCount(item);
			orderList.add(item.getName() + " x " + count);
			total += price * count;
		}
		TextField totalText = (TextField) gui.get("eatcheck.total");
		totalText.setText("" + total);
	}

	void updatePay() {
		List order = (List) gui.get("pay.order");
		order.removeAll();
		int count = 0;
		int total = 0;
		order.removeAll();
		for (Item item : cart.getItems()) {
			int price = item.getPrice();
			count = cart.getItemCount(item);
			order.add(item.getName() + " x " + count);
			total += price * count;
		}
		for (Item item : cart.getItems()) {
			int price = item.getPrice() / 10 * 7;
			count = cart.getoffItemCount(item);
			order.add(item.getName() + "(bring)x " + count);
			total += price * count;
		}
		for (Eat item : cart.geteatItems()) {
			int price = item.getPrice();
			count = cart.geteatItemCount(item);
			order.add(item.getName() + " x " + count);
			total += price * count;
		}
		TextField totalText = (TextField) gui.get("pay.total");
		totalText.setText("" + total);

	}

	void updateReceipt() {
		TextField creditText = (TextField) gui.get("pay.credit");
		String credit = creditText.getText();
		TextField holderText = (TextField) gui.get("pay.holder");
		String holder = holderText.getText();
		cart.setCustomer(holder);
		TextArea receipt = (TextArea) gui.get("receipt.receipt");
		receipt.setText(name + "\n");
		receipt.append("Dear " + holder + "\n");
		if (take != (null) && take.equals("Take out")) {
			receipt.setText("Take out" + "\n");
		}
		receipt.append("Thank you for shopping.\n");
		int total = 0;
		int waittime = 0;
		for (Item item : cart.getItems()) {
			int price = item.getPrice();
			int count = cart.getItemCount(item);
			int time = item.getTime();
			receipt.append(item.getName() + " @" + price + " x " + count
					+ " = " + (price * count) + "\n");
			waittime += time * count;
			total += price * count;
		}
		for (Item item2 : cart.getoffItems()) {
			int price = item2.getPrice() / 10 * 7;
			int count = cart.getoffItemCount(item2);
			receipt.append(item2.getName() + " @" + price + "(bring) x "
					+ count + " = " + (price * count) + "\n");

			total += price * count;
		}
		for (Eat item : cart.geteatItems()) {
			int price = item.getPrice();
			int count = cart.geteatItemCount(item);
			receipt.append(item.getName() + " @" + price + " x " + count
					+ " = " + (price * count) + "\n");

			total += price * count;
		}

		receipt.append("Total: " + total + "\n");
		receipt.append("Waiting time: " + waittime + "minute" + "\n");
		receipt.append("payed by credit card xxxx-xxxx-xxxx-"
				+ credit.substring(credit.length() - 4) + "\n");
		receipt.append("received as the order #" + cart.getId());
	}

	@Override
	public void itemStateChanged(ItemEvent e) {
		if (e.getSource() == c1) {
			s = c1.getSelectedItem();
		}
		if (e.getSource() == gui.get("exp")) {
			Checkbox c1 = (Checkbox) gui.get("exp");
			drink = c1.getLabel();
		}
		if (e.getSource() == gui.get("rob")) {
			Checkbox c2 = (Checkbox) gui.get("rob");
			drink = c2.getLabel();
		}
		if (e.getSource() == gui.get("ara")) {
			Checkbox c3 = (Checkbox) gui.get("ara");
			drink = c3.getLabel();
		}
		if (e.getSource() == gui.get("java")) {
			Checkbox c4 = (Checkbox) gui.get("java");
			drink = c4.getLabel();
		}

		if (e.getSource() == gui.get("order.item")) {
			Item item = getSelectedItem();
			if (item != null) {
				int price = item.getPrice();
				TextField countText = (TextField) gui.get("order.count");
				countText.setText("1");
				TextField totalText = (TextField) gui.get("order.total");
				totalText.setText("" + price);
			}
		}

		if (e.getSource() == gui.get("eat.item")) {
			Eat item2 = getSelectedEat();
			if (item2 != null) {
				int price = item2.getPrice();
				TextField countText = (TextField) gui.get("eat.count");
				countText.setText("1");
				TextField eattotalText = (TextField) gui.get("eat.total");
				eattotalText.setText("" + price);
			}
		}
		if (e.getSource() == gui.get("s.item")) {
			Item item = getSItem();
			if (item != null) {
				int price = item.getPrice() / 10 * 7;
				TextField countText = (TextField) gui.get("s.count");
				countText.setText("1");
				TextField totalText = (TextField) gui.get("s.total");
				totalText.setText("" + price);
			}
		}
		if (e.getSource() == gui.get("m.item")) {
			Item item = getMItem();
			if (item != null) {
				int price = item.getPrice() / 10 * 7;
				TextField countText = (TextField) gui.get("m.count");
				countText.setText("1");
				TextField totalText = (TextField) gui.get("m.total");
				totalText.setText("" + price);
			}
		}
		if (e.getSource() == gui.get("l.item")) {
			Item item = getLItem();
			if (item != null) {
				int price = item.getPrice() / 10 * 7;
				TextField countText = (TextField) gui.get("l.count");
				countText.setText("1");
				TextField totalText = (TextField) gui.get("l.total");
				totalText.setText("" + price);
			}
		}
	}

	Eat getSelectedEat() {
		List itemList = (List) gui.get("eat.item");
		String name = itemList.getSelectedItem();
		if (name == null)
			return null;
		String[] names = name.split("\\s+");
		Eat item2 = EatDB.search(names[0]);
		return item2;
	}

	Item getSelectedItem() {
		List itemList = (List) gui.get("order.item");
		String name = itemList.getSelectedItem();
		if (name == null)
			return null;
		String[] names = name.split("\\s+");
		Item item = ItemDB.search(names[0]);
		return item;
	}

	Item getSItem() {
		List itemList = (List) gui.get("s.item");
		String name = itemList.getSelectedItem();
		if (name == null)
			return null;
		String[] names = name.split("\\s+");
		Item item = ItemDB.search(names[0]);
		return item;
	}

	Item getMItem() {
		List itemList = (List) gui.get("m.item");
		String name = itemList.getSelectedItem();
		if (name == null)
			return null;
		String[] names = name.split("\\s+");
		Item item = ItemDB.search(names[0]);
		return item;
	}

	Item getLItem() {
		List itemList = (List) gui.get("l.item");
		String name = itemList.getSelectedItem();
		if (name == null)
			return null;
		String[] names = name.split("\\s+");
		Item item = ItemDB.search(names[0]);
		return item;
	}

	Eat[] getSelectedeatItems() {
		List orderList = (List) gui.get("eatcheck.order");
		int[] indexes = orderList.getSelectedIndexes();
		if (indexes == null)
			return null;
		Eat[] items = new Eat[indexes.length];
		int n = 0;
		for (int i : indexes) {
			String name = orderList.getItem(i);
			String[] names = name.split("\\s+");
			Eat item = EatDB.search(names[0]);
			items[n++] = item;
		}
		return items;
	}

	Item[] getSelectedItems() {
		List orderList = (List) gui.get("check.order");
		int[] indexes = orderList.getSelectedIndexes();
		if (indexes == null)
			return null;
		Item[] items = new Item[indexes.length];
		int n = 0;
		for (int i : indexes) {
			String name = orderList.getItem(i);
			String[] names = name.split("\\s+");
			Item item = ItemDB.search(names[0]);
			items[n++] = item;
		}
		return items;
	}

	Item[] getSelectedoffItems() {
		List offorderList = (List) gui.get("check.offorder");
		int[] indexes = offorderList.getSelectedIndexes();
		if (indexes == null)
			return null;
		Item[] items = new Item[indexes.length];
		int n = 0;
		for (int i : indexes) {
			String name = offorderList.getItem(i);
			String[] names = name.split("\\s+");
			Item item = ItemDB.search(names[0]);
			items[n++] = item;
		}
		return items;
	}

}
// 逋ｺ螻戊ｪｲ鬘・ｽ
// 1. 謖√■蟶ｰ繧・ｽ(take out)繧ｪ繝励す繝ｧ繝ｳ繧定ｿｽ蜉・ｽ縺励◆縺・ｽ縲・ｽ
// 2. 謖√■霎ｼ縺ｿ(bring your own cup)繧ｪ繝励す繝ｧ繝ｳ繧定ｿｽ蜉・ｽ縺励◆縺・ｽ縲・ｽ
// 3. 蝠・ｽ蜩√・ｽｮ螳梧・ｽ先凾髢薙ｒ莠域ｸｬ縺励・ｽ∝女縺大叙繧雁ｾ・ｽ縺｡縺ｮ譎る俣繧・ｽ0縺ｫ縺励◆縺・ｽ縲・ｽ
// 4. 鬟溷刀繝｡繝九Η繝ｼ繧貞・ｽ・ｽ螳溘＆縺帙◆縺・ｽ縲・ｽ
// 5. 繝ｦ繝ｼ繧ｶ繧｢繧ｫ繧ｦ繝ｳ繝医ｒ險ｭ縺代・ｽ√け繝ｬ繧ｸ繝・ｽ繝域ュ蝣ｱ繧剃ｿ晏ｭ倥＠縲∵髪謇輔＞繧堤ｰ｡蜊倥↓縺励◆縺・ｽ縲・ｽ
// 6. 繝ｦ繝ｼ繧ｶ縺ｮ螂ｽ縺ｿ繧貞庶髮・ｽ縺励◆縺・ｽ縲・ｽ
// 7. 繝ｦ繝ｼ繧ｶ縺ｫ蠎・ｽ蜻翫Γ繝ｼ繝ｫ繧帝・ｽ√ｊ縺溘＞縲・ｽ

