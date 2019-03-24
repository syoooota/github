package shop;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// クレジット会社のモックアップモデル
public class CreditDB {
	static List<Credit> credits = new ArrayList<Credit>();
	static Map<String,Credit> nameIndex = new HashMap<String,Credit>();
	static Map<String,Credit> passIndex = new HashMap<String,Credit>();
	static {
		Credit[] credits={
			//number, holder,datem,datey,pass
			new Credit("3867012370799347","shota","01","11","1234"),
		};
		for(Credit credit : credits) {
			register(credit);
		}
	}




	public static void register(Credit item) {
		synchronized(credits) {
			int no = credits.size();
			item.setId(no);
			credits.add(item);

			nameIndex.put(item.getHolder(), item);
			passIndex.put(item.getPass(), item);
		}
	}

	public static Credit search(int id) {
		synchronized(credits) {
			return credits.get(id);
		}
	}

	public static Credit search3(String holder) {
		synchronized(credits) {
			return nameIndex.get(holder);
		}
	}

	public static Credit search2(String pass) {
		synchronized(credits) {
			return passIndex.get(pass);
		}
	}
	public static boolean canPay(String number, String holder, String date) {
		// dummy
		return true;
	}

}
