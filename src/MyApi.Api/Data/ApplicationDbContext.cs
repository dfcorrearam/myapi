using Microsoft.EntityFrameworkCore;
using MyApi.Api.Domain;
using MyApi.Api.Entities;

namespace MyApi.Api.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<WeatherForecast> WeatherForecasts => Set<WeatherForecast>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<WeatherForecast>(entity =>
        {
            entity.Property(e => e.Summary)
                  .HasMaxLength(500); // o 255, lo que tenga sentido
        });
    }
}
