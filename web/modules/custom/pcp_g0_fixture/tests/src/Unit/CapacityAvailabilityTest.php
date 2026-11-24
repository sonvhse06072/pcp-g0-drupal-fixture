<?php

namespace Drupal\Tests\pcp_g0_fixture\Unit;

use Drupal\Core\Config\Config;
use Drupal\Core\Config\ConfigFactoryInterface;
use Drupal\pcp_g0_fixture\CapacityAvailability;
use Drupal\Tests\UnitTestCase;
use PHPUnit\Framework\Attributes\Group;

/**
 * Tests capacity arithmetic and input validation.
 *
 * @coversDefaultClass \Drupal\pcp_g0_fixture\CapacityAvailability
 */
#[Group('pcp_g0_fixture')]
final class CapacityAvailabilityTest extends UnitTestCase {

  /**
   * Checks ordinary availability arithmetic.
   */
  #[\PHPUnit\Framework\Attributes\DataProvider('capacityCases')]
  public function testRemaining(int $capacity, int $booked, int $expected): void {
    $config = $this->createMock(Config::class);
    $config->method('get')->with('capacity')->willReturn($capacity);
    $factory = $this->createMock(ConfigFactoryInterface::class);
    $factory->method('get')->with('pcp_g0_fixture.capacity')->willReturn($config);
    self::assertSame($expected, (new CapacityAvailability($factory))->remaining($booked));
  }

  /**
   * Provides capacity arithmetic cases.
   *
   * @return array<string, array{int, int, int}>
   *   The test cases.
   */
  public static function capacityCases(): array {
    return [
      'empty' => [25, 0, 25],
      'one left' => [25, 24, 1],
      'full' => [25, 25, 0],
      'overbooked' => [25, 26, 0],
    ];
  }

  /**
   * Rejects invalid supplied counts and configuration values.
   */
  #[\PHPUnit\Framework\Attributes\DataProvider('invalidCases')]
  public function testInvalidInput(mixed $capacity, int $booked): void {
    $config = $this->createMock(Config::class);
    $config->method('get')->with('capacity')->willReturn($capacity);
    $factory = $this->createMock(ConfigFactoryInterface::class);
    $factory->method('get')->with('pcp_g0_fixture.capacity')->willReturn($config);
    $this->expectException(\InvalidArgumentException::class);
    (new CapacityAvailability($factory))->remaining($booked);
  }

  /**
   * Provides invalid input cases.
   *
   * @return array<string, array{mixed, int}>
   *   The test cases.
   */
  public static function invalidCases(): array {
    return [
      'negative capacity' => [-1, 0],
      'non-integer capacity' => ['10', 0],
      'negative booked' => [10, -1],
    ];
  }

  /**
   * Missing configured capacity means no availability.
   */
  public function testMissingCapacity(): void {
    $config = $this->createMock(Config::class);
    $config->method('get')->with('capacity')->willReturn(NULL);
    $factory = $this->createMock(ConfigFactoryInterface::class);
    $factory->method('get')->with('pcp_g0_fixture.capacity')->willReturn($config);
    self::assertSame(0, (new CapacityAvailability($factory))->remaining(0));
  }

}
