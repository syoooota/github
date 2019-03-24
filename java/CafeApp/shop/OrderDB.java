package shop;

import java.util.ArrayList;
import java.util.List;

public class OrderDB {
	static List<Order> orders = new ArrayList<Order>();

	public static void accept(Order order) {
		synchronized (orders) {
			int no = orders.size();
			order.setId(no);
			orders.add(order);
		}
	}

	public static Order search(int no) {
		synchronized (orders) {
			return orders.get(no);
		}
	}

}
