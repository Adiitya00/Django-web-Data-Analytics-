from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('process_file')
    else:
        form = UploadFileForm()
    return render(request, 'myapp/templates/upload_file.html', {'form': form})

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render


def process_file(request):
    # Get the latest uploaded file
    uploaded_file = UploadedFile.objects.latest('id')
    file_path = uploaded_file.file.path  # Get the file path
    
    # Read the CSV file using pandas
    df = pd.read_csv(file_path)
    
    # Display the first few rows of the data
    first_rows = df.head().to_html()
    
    # Calculate summary statistics for numerical columns
    summary_stats = df.describe().to_html()
    
    # Calculate mean, median, and standard deviation for numerical columns
    mean = df.mean().to_frame(name='Mean').T.to_html()
    median = df.median().to_frame(name='Median').T.to_html()
    std_dev = df.std().to_frame(name='Standard Deviation').T.to_html()
    
    # Identify missing values
    missing_values = df.isnull().sum().to_frame(name='Missing Values').T.to_html()
    
    # Generate basic plots using seaborn and matplotlib
    plot_path = 'media/histogram.png'
    sns.histplot(df.select_dtypes(include='number').melt(), kde=True)
    plt.savefig(plot_path)
    plt.close()

    # Context to pass to the template
    context = {
        'first_rows': first_rows,
        'summary_stats': summary_stats,
        'mean': mean,
        'median': median,
        'std_dev': std_dev,
        'missing_values': missing_values,
        'plot_path': plot_path,
    }

    return render(request, 'myapp/templates/analysis_results.html', context)
