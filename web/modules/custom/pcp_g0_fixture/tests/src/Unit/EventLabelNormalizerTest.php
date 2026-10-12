<?php

namespace Drupal\Tests\pcp_g0_fixture\Unit;

use Drupal\pcp_g0_fixture\EventLabelNormalizer;
use Drupal\Tests\UnitTestCase;
use PHPUnit\Framework\Attributes\Group;

/**
 * Tests the isolated normalizer.
 *
 * @coversDefaultClass \Drupal\pcp_g0_fixture\EventLabelNormalizer
 */
#[Group('pcp_g0_fixture')]
final class EventLabelNormalizerTest extends UnitTestCase {

  /**
   * Tests a normal label.
   */
  public function testOrdinaryLabel(): void {
    self::assertSame('Acoustic', (new EventLabelNormalizer())->normalize('Acoustic'));
  }

  /**
   * Tests trimming and collapsing consecutive internal ASCII whitespace.
   */
  public function testTrimsOuterWhitespace(): void {
    self::assertSame('Jazz Band', (new EventLabelNormalizer())->normalize(" \tJazz Band\n "));
  }

  /**
   * Tests collapsing consecutive internal tabs and CR/LF characters.
   */
  public function testCollapsesInternalTabsAndLineBreaks(): void {
    self::assertSame('Jazz Band Live', (new EventLabelNormalizer())->normalize("Jazz\t\tBand\r\n\nLive"));
  }

  /**
   * Tests that nonbreaking spaces are preserved.
   */
  public function testPreservesNonbreakingSpaces(): void {
    self::assertSame("Jazz\u{00A0}\u{00A0}Band", (new EventLabelNormalizer())->normalize("Jazz\u{00A0}\u{00A0}Band"));
  }

}
