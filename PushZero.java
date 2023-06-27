
import java.io.*;

public class PushZero
{
	static void pushZerosToRight(int arr[], int n)
	{
		int count = 0; // Count of non-zero elements

		for (int i = 0; i < n; i++)
			if (arr[i] != 0)
				arr[count++] = arr[i]; 
		while (count < n)
			arr[count++] = 0;
	}

	
	public static void main (String[] args)
	{
		int arr[] = {0,1,0,3,12};
		int n = arr.length;
		pushZerosToRight(arr, n);
		System.out.println("Array after pushing zeros to the right ");
		for (int i=0; i<n; i++)
			System.out.print(arr[i]+" ");
	}
}
