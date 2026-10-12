<?php

namespace Drupal\pcp_g0_fixture;

/**
 * Normalizes a fixture label without external dependencies.
 *
 * Collapses consecutive internal ASCII whitespace into a single space.
 */
final class EventLabelNormalizer {

  /**
   * Trims surrounding whitespace and collapses internal ASCII whitespace.
   */
  public function normalize(string $label): string {
    return preg_replace('/[ \t\r\n]+/', ' ', trim($label));
  }

}
