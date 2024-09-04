# Import the necessary libraries
import matplotlib.pyplot as plt  # For creating static, animated, and interactive visualizations in Python
from IPython import display  # For displaying output in Jupyter notebooks

# Turn the interactive mode on. This means that any plt.plot() command will cause a figure window to open, 
# and further commands can be run to update the plot. Some changes (such as modifying properties of lines 
# that are already drawn) will not draw automatically, in these cases, you should use plt.draw() to force an update.
plt.ion()

# Define a function to plot scores and mean scores
def plot(scores, mean_scores):
    # Clear the output of the current cell receiving output
    display.clear_output(wait=True)
    # Display the figure defined by plt.gcf() (get current figure). If no current figure exists, a new one is created.
    display.display(plt.gcf())
    # Clear the current figure. If no figure exists, a new one is created.
    plt.clf()
    # Set the title of the current figure
    plt.title('Training...')
    # Set the label for the x-axis
    plt.xlabel('Number of Games')
    # Set the label for the y-axis
    plt.ylabel('Score')
    # Plot the scores
    plt.plot(scores)
    # Plot the mean scores
    plt.plot(mean_scores)
    # Set the limits of the y-axis. ymin=0 means the y-axis starts at 0.
    plt.ylim(ymin=0)
    # Add a text at the end of the scores plot, displaying the last score
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    # Add a text at the end of the mean scores plot, displaying the last mean score
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    # Display the figure but do not block the execution of the rest of the code
    plt.show(block=False)
    # Pause the execution of the code for 0.1 seconds. This is often used for updating a plot in an animated fashion.
    plt.pause(.1)