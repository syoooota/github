package shop;

public class Credit {
	String number, holder, pass,datem,datey;
	int id ;

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public Credit(String number, String holder, String datem,String datey,String pass) {
		this.number = number;
		this.holder = holder;
		this.datem = datem;
		this.datey = datey;
		this.pass = pass;
	}



	public String getDatem() {
		return datem;
	}

	public void setDatem(String datem) {
		this.datem = datem;
	}

	public String getDatey() {
		return datey;
	}

	public void setDatey(String datey) {
		this.datey = datey;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((datem == null) ? 0 : datem.hashCode());
		result = prime * result + ((datey == null) ? 0 : datey.hashCode());
		result = prime * result + ((holder == null) ? 0 : holder.hashCode());
		result = prime * result + id;
		result = prime * result + ((number == null) ? 0 : number.hashCode());
		result = prime * result + ((pass == null) ? 0 : pass.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Credit other = (Credit) obj;
		if (datem == null) {
			if (other.datem != null)
				return false;
		} else if (!datem.equals(other.datem))
			return false;
		if (datey == null) {
			if (other.datey != null)
				return false;
		} else if (!datey.equals(other.datey))
			return false;
		if (holder == null) {
			if (other.holder != null)
				return false;
		} else if (!holder.equals(other.holder))
			return false;
		if (id != other.id)
			return false;
		if (number == null) {
			if (other.number != null)
				return false;
		} else if (!number.equals(other.number))
			return false;
		if (pass == null) {
			if (other.pass != null)
				return false;
		} else if (!pass.equals(other.pass))
			return false;
		return true;
	}

	public String getPass() {
		return pass;
	}

	public void setPass(String pass) {
		this.pass = pass;
	}

	public String getNumber() {
		return number;
	}

	public void setNumber(String number) {
		this.number = number;
	}

	public String getHolder() {
		return holder;
	}

	public void setHolder(String holder) {
		this.holder = holder;
	}

}
