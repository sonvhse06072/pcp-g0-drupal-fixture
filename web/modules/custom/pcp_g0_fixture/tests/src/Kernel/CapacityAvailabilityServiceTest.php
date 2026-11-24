<?php

namespace Drupal\Tests\pcp_g0_fixture\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Drupal\pcp_g0_fixture\CapacityAvailability;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\Attributes\RunTestsInSeparateProcesses;

/**
 * Tests configuration-backed capacity in Drupal's kernel.
 */
#[Group('pcp_g0_fixture')]
#[RunTestsInSeparateProcesses]
final class CapacityAvailabilityServiceTest extends KernelTestBase {

  /**
   * {@inheritdoc}
   */
  protected static $modules = ['pcp_g0_fixture'];

  /**
   * Tests service wiring, defaults, cache metadata, and config invalidation.
   */
  public function testConfiguredCapacityAndCacheMetadata(): void {
    $this->installConfig(['pcp_g0_fixture']);
    $service = $this->container->get('pcp_g0_fixture.capacity_availability');
    self::assertInstanceOf(CapacityAvailability::class, $service);
    self::assertSame(25, $service->remaining(0));
    self::assertSame(1, $service->remaining(24));
    self::assertSame(0, $service->remaining(25));
    self::assertSame(0, $service->remaining(26));

    self::assertContains('config:pcp_g0_fixture.capacity', $service->getCacheTags());
    self::assertSame(-1, $service->getCacheMaxAge());
    self::assertSame([], $service->getCacheContexts());

    $this->config('pcp_g0_fixture.capacity')->set('capacity', 10)->save();
    self::assertSame(10, $service->remaining(0));
  }

}
