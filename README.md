import java.util.Scanner;

public class Cuadrantes {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = leerCantidad(sc);

        int c1 = 0, c2 = 0, c3 = 0, c4 = 0;

        for (int i = 1; i <= n; i++) {
            double x = leerCoordenada(sc, "X");
            double y = leerCoordenada(sc, "Y");

            int cuadrante = obtenerCuadrante(x, y);

            if (cuadrante == 1) {
                c1++;
            } else if (cuadrante == 2) {
                c2++;
            } else if (cuadrante == 3) {
                c3++;
            } else if (cuadrante == 4) {
                c4++;
            }
        }

        mostrarResultados(c1, c2, c3, c4);
    }

    public static int leerCantidad(Scanner sc) {
        System.out.print("Ingrese cantidad de puntos: ");
        return sc.nextInt();
    }

    public static double leerCoordenada(Scanner sc, String nombre) {
        System.out.print(nombre + ": ");
        return sc.nextDouble();
    }

    public static int obtenerCuadrante(double x, double y) {
        if (x > 0 && y > 0) {
            return 1;
        } else if (x < 0 && y > 0) {
            return 2;
        } else if (x < 0 && y < 0) {
            return 3;
        } else if (x > 0 && y < 0) {
            return 4;
        } else {
            return 0;
        }
    }

    public static void mostrarResultados(int c1, int c2, int c3, int c4) {
        System.out.println("Puntos en el primer cuadrante: " + c1);
        System.out.println("Puntos en el segundo cuadrante: " + c2);
        System.out.println("Puntos en el tercer cuadrante: " + c3);
        System.out.println("Puntos en el cuarto cuadrante: " + c4);
    }
}
