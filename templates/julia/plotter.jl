using Plots

x = 0.01:0.01:0.1       # Avoid x=0 to prevent division by zero and log(0)
# y = (1 ./ x) .* log.(1 ./ x)
y = (1 ./ x) .* log.(1 ./ x)

# Create the plot
plot(x, y, title="Sample Plot", xlabel="X Axis", ylabel="Y Axis", label="Return Data", lw=2, marker=:circle)

# Save the plot as a PNG file
savefig("sample_plot.png")