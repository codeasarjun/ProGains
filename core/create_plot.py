
import matplotlib.pyplot as plt
import io
import base64

def visulize_data(rd_spend, administration, marketing_spend):
# Generate a simple plot
    plt.figure(figsize=(8, 6))
    plt.bar(["R&D Spend", "Administration", "Marketing Spend"], [rd_spend, administration, marketing_spend], color=['blue', 'green', 'orange'])
    plt.xlabel("Features")
    plt.ylabel("Values")
    plt.title("Input Features")
    
    # Save plot to a bytes object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

    