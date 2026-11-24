<?php

namespace Drupal\pcp_g0_fixture;

use Drupal\Core\Cache\CacheableDependencyInterface;
use Drupal\Core\Config\ConfigFactoryInterface;

/**
 * Calculates remaining fixture capacity from immutable configuration.
 */
final class CapacityAvailability implements CacheableDependencyInterface {

  /**
   * Constructs the availability calculator.
   */
  public function __construct(
    private readonly ConfigFactoryInterface $configFactory,
  ) {}

  /**
   * Returns remaining capacity after the supplied number of bookings.
   */
  public function remaining(int $booked): int {
    if ($booked < 0) {
      throw new \InvalidArgumentException('Booked count cannot be negative.');
    }

    $capacity = $this->configFactory->get('pcp_g0_fixture.capacity')->get('capacity');
    if ($capacity === NULL) {
      return 0;
    }
    if (!is_int($capacity) || $capacity < 0) {
      throw new \InvalidArgumentException('Configured capacity must be a non-negative integer.');
    }

    return max(0, $capacity - $booked);
  }

  /**
   * {@inheritdoc}
   */
  public function getCacheContexts(): array {
    return [];
  }

  /**
   * {@inheritdoc}
   */
  public function getCacheTags(): array {
    return $this->configFactory->get('pcp_g0_fixture.capacity')->getCacheTags();
  }

  /**
   * {@inheritdoc}
   */
  public function getCacheMaxAge(): int {
    return $this->configFactory->get('pcp_g0_fixture.capacity')->getCacheMaxAge();
  }

}
