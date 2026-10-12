<?php

namespace Drupal\Tests\pcp_g0_fixture\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Drupal\pcp_g0_fixture\EventLabelNormalizer;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\Attributes\RunTestsInSeparateProcesses;

/**
 * Tests the fixture normalizer as a Drupal Kernel service.
 */
#[Group('pcp_g0_fixture')]
#[RunTestsInSeparateProcesses]
final class EventLabelServiceTest extends KernelTestBase {

  /**
   * {@inheritdoc}
   */
  protected static $modules = ['pcp_g0_fixture'];

  /**
   * Tests actual service wiring and baseline behavior.
   */
  public function testServiceRegistration(): void {
    $service = $this->container->get('pcp_g0_fixture.event_label_normalizer');
    self::assertInstanceOf(EventLabelNormalizer::class, $service);
    self::assertSame('Stage', $service->normalize(' Stage '));
  }

  /**
   * Tests normalization of ASCII whitespace through the registered service.
   */
  public function testServiceCollapsesInternalWhitespace(): void {
    $service = $this->container->get('pcp_g0_fixture.event_label_normalizer');
    self::assertSame('Stage Door', $service->normalize("Stage\t\tDoor\r\n"));
  }

  /**
   * Tests that the registered service preserves nonbreaking spaces.
   */
  public function testServicePreservesNonbreakingSpaces(): void {
    $service = $this->container->get('pcp_g0_fixture.event_label_normalizer');
    self::assertSame("Stage\u{00A0}\u{00A0}Door", $service->normalize("Stage\u{00A0}\u{00A0}Door"));
  }

}
