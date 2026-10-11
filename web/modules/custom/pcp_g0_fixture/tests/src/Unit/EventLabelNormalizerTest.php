<?php

namespace Drupal\Tests\pcp_g0_fixture\Unit;

use Drupal\pcp_g0_fixture\EventLabelNormalizer;
use Drupal\Tests\UnitTestCase;
use PHPUnit\Framework\Attributes\Group;

/**
 * Tests the isolated normalizer on ordinary labels only.
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
   * Tests trimming and normalization of internal ASCII whitespace.
   */
  public function testTrimsOuterWhitespace(): void {
    self::assertSame('Jazz Band', (new EventLabelNormalizer())->normalize(" \tJazz Band\n "));
  }

  /**
   * Tests collapsing consecutive internal tabs and CR/LF characters.
   */
  public function testCollapsesInternalAsciiWhitespace(): void {
    self::assertSame('Jazz Band Stage', (new EventLabelNormalizer())->normalize("Jazz\t\tBand\r\n\nStage"));
  }

  /**
   * Tests that nonbreaking spaces are preserved.
   */
  public function testPreservesNonbreakingSpaces(): void {
    $label = "Jazz\u{00A0}\u{00A0}Band";
    self::assertSame($label, (new EventLabelNormalizer())->normalize($label));
  }

}
