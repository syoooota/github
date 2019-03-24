package kadai;

import java.applet.Applet;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.HashMap;

@SuppressWarnings("serial")
public class Shoot extends Applet implements Runnable, KeyListener {
	private static final long SPEED = 200;

	private static final int block = 10;
	int me = 20;
	int start = 0;

	private static final int screen_height = 20;
	int x = 0;
	int y = 0;
	int z = 0;
	int x1 = 0;
	int y1 = 0;
	int z1 = 0;

	static char[] types = { 'J', 'L', 'S', 'Z', 'T' };
	static HashMap<Character, Color> colors;
	static {
		colors = new HashMap<Character, Color>();

	}

	private Thread th = null;
	char type;
	char type2;
	char type3;

	char[][] screen;

	boolean isGameOver = false;

	public void init() {
		setSize(200, 270);
		addKeyListener(this);
		choice1();
		choice2();
		choice3();
		screen = new char[screen_height][10];
		clear();
	}

	public void start() {
		if (th == null) {
			th = new Thread(this);
			th.start();
		}
	}

	public void stop() {
		if (th != null) {
			th = null;
		}
	}

	void clear() {
		for (int y = 0; y < screen.length; y++)
			for (int x = 0; x < screen[y].length; x++)
				screen[y][x] = ' ';
	}

	int xx = 10;
	int yy = 20;
	int zz = 30;

	public void paint(Graphics g) {

		if (start == 1){
		g.setColor(Color.WHITE);
		g.fillRect(0, 0, 50, 200);

		g.setColor(Color.blue);
		g.fill3DRect(70, 30, 20, 20, true);

		g.setColor(Color.green);
		g.fill3DRect(110, 30, 20, 20, true);

		g.setColor(Color.red);
		g.fill3DRect(150, 30, 20, 20, true);

		g.setColor(Color.magenta);
		g.fill3DRect(70, 60, 20, 20, true);

		

		if (type == 'J') {
			g.setColor(Color.blue);
			g.fill3DRect(xx, x, block, block, true);

		} else if (type == 'L') {

			g.setColor(Color.green);
			g.fill3DRect(xx, x, block, block, true);
		} else if (type == 'S') {

			g.setColor(Color.red);
			g.fill3DRect(xx, x, block, block, true);
		} else if (type == 'Z') {

			g.setColor(Color.magenta);
			g.fill3DRect(xx, x, block, block, true);
		} else if (type == 'T') {
			x = 0;
			g.setColor(Color.gray);
			g.fill3DRect(xx, x1, block, block, true);
		}

		if (type2 == 'J') {
			g.setColor(Color.blue);
			g.fill3DRect(yy, y, block, block, true);

		} else if (type2 == 'L') {

			g.setColor(Color.green);
			g.fill3DRect(yy, y, block, block, true);
		} else if (type2 == 'S') {

			g.setColor(Color.red);
			g.fill3DRect(yy, y, block, block, true);
		} else if (type2 == 'Z') {

			g.setColor(Color.magenta);
			g.fill3DRect(yy, y, block, block, true);
		} else if (type2 == 'T') {
			y = 0;
			g.setColor(Color.gray);
			g.fill3DRect(yy, y1, block, block, true);
		}

		if (type3 == 'J') {
			g.setColor(Color.blue);
			g.fill3DRect(zz, z, block, block, true);

		} else if (type3 == 'L') {

			g.setColor(Color.green);
			g.fill3DRect(zz, z, block, block, true);
		} else if (type3 == 'S') {

			g.setColor(Color.red);
			g.fill3DRect(zz, z, block, block, true);
		} else if (type3 == 'Z') {

			g.setColor(Color.magenta);
			g.fill3DRect(zz, z, block, block, true);
		} else if (type3 == 'T') {
			z = 0;
			g.setColor(Color.gray);
			g.fill3DRect(zz, z1, block, block, true);
		}
		g.setColor(Color.black);
		g.fill3DRect(me, 200, block, block, false);
		g.drawString("=1", 90, 40);
		g.drawString("=2", 130, 40);
		g.drawString("=3", 170, 40);
		g.drawString("=4", 90, 70);

		if (z == 200) {
			g.setColor(Color.red);
			g.drawString("Game Over", 120, 100);
		}
		if (y == 200) {
			g.setColor(Color.red);
			g.drawString("Game Over", 120, 100);
		}
		if (x == 200) {
			g.setColor(Color.red);
			g.drawString("Game Over", 120, 100);
		}
		if (me == xx) {
			if (200 == x1) {
				g.setColor(Color.red);
				g.drawString("Game Over", 120, 100);
			}
		}
		if (me == yy) {
			if (200 == y1) {
				g.setColor(Color.red);
				g.drawString("Game Over", 120, 100);
			}
		}
		if (me == zz) {
			if (200 == z1) {

				g.setColor(Color.red);
				g.drawString("Game Over", 120, 100);
			}
		}
		}else if (start == 0) {
				g.setColor(Color.red);
				g.drawString("Push Enter key", 50, 100);
		}

	}

	void owari() {
		if (me == xx) {
			if (200 == x1) {
				stop();
				repaint();
			}
		}
		if (me == yy) {
			if (200 == y1) {
				stop();
				repaint();
			}
		}
		if (me == zz) {
			if (200 == z1) {

				stop();
				repaint();
			}
		}
		if (x == 200) {
			stop();
			repaint();
		}
		if (y == 200) {

			stop();
			repaint();
		}
		if (z == 200) {

			stop();
			repaint();
		}

	}

	void choice1() {
		type = types[(int) (Math.random() * types.length)];
		if (type == type2) {
			type = types[(int) (Math.random() * types.length)];
		}

	}

	void choice2() {
		type2 = types[(int) (Math.random() * types.length)];

		if (type == type2) {
			type2 = types[(int) (Math.random() * types.length)];
		} else if (type2 == type3) {
			type2 = types[(int) (Math.random() * types.length)];
		}
	}

	void choice3() {
		type3 = types[(int) (Math.random() * types.length)];

		if (type2 == type3) {
			type3 = types[(int) (Math.random() * types.length)];
		}
	}

	@Override
	public void run() {
		
		while (th == Thread.currentThread()) {
			try {
				Thread.sleep(SPEED);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			
			repaint();
                        if (start == 1){
			x = x + 10;
			y = y + 10;
			z = z + 10;
			x1 = x1 + 10;
			y1 = y1 + 10;
			z1 = z1 + 10;
			owari();
			if (x1 == 200) {
				x1 = 0;
				choice1();
				repaint();

			}
			if (y1 == 200) {
				y1 = 0;
				choice1();
				repaint();

			}
			if (z1 == 200) {
				z1 = 0;
				choice1();
				repaint();

			}
			}
			
		}
	}
	
	@Override
	public void keyTyped(KeyEvent e) {
	}

	@Override
	public void keyPressed(KeyEvent e) {
		if (e.getKeyCode() == KeyEvent.VK_ENTER) {
			start = 1;
		}
		if (e.getKeyCode() == KeyEvent.VK_1) {

			if (me == xx) {
				if (type == 'J') {
					x = 0;
					x1 = 0;
					choice1();
				}
			}
			if (me == yy) {
				if (type2 == 'J') {
					y = 0;
					y1 = 0;
					choice2();
				}
			}
			if (me == zz) {
				if (type3 == 'J') {
					z = 0;
					z1 = 0;
					choice3();

				}
			}
		}
		if (e.getKeyCode() == KeyEvent.VK_2) {

			if (me == xx) {
				if (type == 'L') {
					x = 0;
					x1 = 0;
					choice1();
				}
			}
			if (me == yy) {
				if (type2 == 'L') {
					y = 0;
					y1 = 0;
					choice2();
				}
			}
			if (me == zz) {
				if (type3 == 'L') {
					z = 0;
					z1 = 0;
					choice3();

				}
			}
		}
		if (e.getKeyCode() == KeyEvent.VK_3) {
			if (me == xx) {
				if (type == 'S') {
					x = 0;
					x1 = 0;
					choice1();
				}
			}
			if (me == yy) {
				if (type2 == 'S') {
					y = 0;
					y1 = 0;
					choice2();
				}
			}
			if (me == zz) {
				if (type3 == 'S') {
					z = 0;
					z1 = 0;
					choice3();
				}
			}
		}

		if (e.getKeyCode() == KeyEvent.VK_4) {
			if (me == xx) {
				if (type == 'Z') {
					x = 0;
					x1 = 0;
					choice1();
				}
			}
			if (me == yy) {
				if (type2 == 'Z') {
					y = 0;
					y1 = 0;
					choice2();
				}
			}
			if (me == zz) {
				if (type3 == 'Z') {
					z = 0;
					z1 = 0;
					choice3();
				}
			}
		}

		if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
			if (me < 30) {
				me = me + 10;
	
			}
		}
		if (e.getKeyCode() == KeyEvent.VK_LEFT) {
			if (10 < me) {
				me = me - 10;
			
			}
		}
	}

	@Override
	public void keyReleased(KeyEvent e) {
	}

}